import requests
import pandas as pd
import json
import argparse

from django.core.management.base import BaseCommand, CommandError
from sorare.models import ScoutingResult

class Command(BaseCommand):
    help = 'Executes Sorare API query to find the best scouting result and its price'

    def add_arguments(self, parser):
        parser.add_argument(
            '-p', '--position', default="Forward", nargs='?', type=str, required=True, help='options: Goalkeeper, Defender, Midfielder, Forward'
        )
        parser.add_argument(
            '-l', '--league', default="BUNDESLIGA", nargs='?', type=str, required=True, help='options: BUNDESLIGA, SERIE_A'
        )

    def handle(self, *args, **options):
        league_dict = {
            "BUNDESLIGA": '["bayern-munchen-munchen","borussia-dortmund-dortmund","rb-leipzig-leipzig",\
                              "union-berlin-berlin","freiburg-freiburg-im-breisgau","eintracht-frankfurt-frankfurt-am-main",\
                              "wolfsburg-wolfsburg","borussia-m-gladbach-monchengladbach","bayer-leverkusen-leverkusen",\
                              "werder-bremen-bremen","mainz-05-mainz","koln-koln",\
                              "hoffenheim-sinsheim","augsburg-augsburg","stuttgart-stuttgart",\
                              "bochum-bochum","hertha-bsc-berlin","schalke-04-gelsenkirchen"]',
            "SERIE_A": '["juventus-torino","napoli-castel-volturno","milan-milano",\
                            "internazionale-milano","atalanta-ciserano","lazio-formello",\
                            "roma-roma","udinese-udine","torino-torino",\
                            "bologna-bologna","empoli-empoli","fiorentina-firenze",\
                            "monza-monza","salernitana-salerno","lecce-lecce",\
                            "spezia-la-spezia","sassuolo-sassuolo","hellas-verona-verona",\
                            "sampdoria-genova","cremonese-cremona"]',
        }

        query = '''\
            query {\
              allCards(rarities:unique, positions:%s, teamSlugs:%s, first:1000) {\
                nodes {\
                  player {\
                  firstName\
                  lastName\
                  slug\
                  averageScore(type: LAST_FIFTEEN_SO5_AVERAGE_SCORE)\
                  playingStatus\
                  so5Scores(last: 5) {\
                    score\
                    }\
                  }\
                }\
              }\
            }\
        ''' % (options['position'], league_dict[options['league']])

        url = "https://api.sorare.com/graphql/"

        # Send the request and get the response
        response = requests.post(url, json={"query": query}, headers={"APIKEY":"bcda5dc2e53c47ce3b4955e126c0d8c39eb94116f5ae4111fd826b893bbee2bad2d158c1662cbb1c5e711283f8ddb8e11aefdbb2e6cb36454c250390cd4sr128"})

        # Extract the data from the response and save it as a DataFrame
        json_data = json.loads(response.text)
        df_data = json_data["data"]["allCards"]["nodes"]
        df = pd.DataFrame(df_data)

        # Some DataFrame manipulations to remove unnecessary data
        df = df.join(pd.json_normalize(df.pop('player')))
        df = df.join(pd.json_normalize(df.pop('so5Scores')))
        df[4] = df[4].fillna('{}')
        df.pop(0)
        df.pop(1)
        df.pop(2)
        df.pop(3)
        df = df.join(pd.json_normalize(df.pop(4)))
        df.drop_duplicates(subset=['lastName'], keep="first", inplace=True)

        # Calculate difference between average score and fifth last score
        df["dif_average_to_recent_score"] = (df["averageScore"] - df["score"]).where(df['playingStatus'] == "STARTER").where(df['score'] != 0.0)

        # Calculate the maximum difference
        max_dif = df["dif_average_to_recent_score"].idxmax(axis=0, skipna=True)

        # Save data in dictionary
        best_scouting_result = {
            'first_name': df["firstName"][max_dif],
            'last_name': df["lastName"][max_dif],
            'slug': df["slug"][max_dif],
            'league': options['league'],
            'position': options['position'],
            'initial_SO5_average_15': df["averageScore"][max_dif],
            'initial_fifth_last_score': df["score"][max_dif],
            'dif_average_to_recent_score': df["dif_average_to_recent_score"][max_dif]
        }

        # Query the current market offers
        best_price_query = '''\
            query{\
                player(slug:"%s"){\
                    cards(rarities:%s, first:1000){\
                        nodes{\
                            liveSingleSaleOffer{\
                                price\
                            }\
                        }\
                    }\
                }\
            }\
        ''' % (best_scouting_result["slug"], "limited")

        # Send the request and get the response
        response = requests.post(url, json={"query": best_price_query}, headers={
            "APIKEY": "bcda5dc2e53c47ce3b4955e126c0d8c39eb94116f5ae4111fd826b893bbee2bad2d158c1662cbb1c5e711283f8ddb8e11aefdbb2e6cb36454c250390cd4sr128"})

        # Extract the data from the response and save it as a DataFrame
        json_data = json.loads(response.text)
        df_price_data = json_data["data"]["player"]["cards"]["nodes"]

        # Some DataFrame manipulations to remove unnecessary data
        price_df = pd.DataFrame(df_price_data)
        #Error handling, if no offer exists
        try:
            price_df['liveSingleSaleOffer'] = price_df['liveSingleSaleOffer'].fillna('{}')
            price_df = price_df.join(pd.json_normalize(price_df.pop('liveSingleSaleOffer')))
            price_df.dropna(subset=["price"], inplace=True)

            # Convert price from string to integer
            price_df['price'] = price_df['price'].astype(int)

            # Get the floor price
            min_price = price_df["price"].min()

            # Convert price from WEI to ETH
            best_scouting_result["initial_floor_price_limited_ETH"] = min_price / 1000000000000000000.0
        except:
            best_scouting_result["initial_floor_price_limited_ETH"] = 0

        # Get current ETH exchange rate and calculate EUR value
        coinbase_url = "https://api.coinbase.com/v2/exchange-rates?currency=ETH"
        response = requests.get(coinbase_url)
        ETH_EUR = float(json.loads(response.text)["data"]["rates"]["EUR"])
        best_scouting_result["initial_floor_price_limited_EUR"] = best_scouting_result["initial_floor_price_limited_ETH"] * ETH_EUR

        ScoutingResult.objects.create(
            firstName=best_scouting_result["first_name"],
            lastName=best_scouting_result["last_name"],
            playerSlug=best_scouting_result["slug"],
            initialSO5average15=best_scouting_result["initial_SO5_average_15"],
            initialFifthLastScore=best_scouting_result["initial_fifth_last_score"],
            league=best_scouting_result["league"],
            position=best_scouting_result["position"],
            initialFloorPriceLimitedETH=best_scouting_result["initial_floor_price_limited_ETH"],
            initialFloorPriceLimitedEUR=best_scouting_result["initial_floor_price_limited_EUR"],
        )

