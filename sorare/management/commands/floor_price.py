import requests
import pandas as pd
import json

from django.core.management.base import BaseCommand, CommandError
from sorare.models import FloorPrice, ScoutingResult
from sorare.constants import best_price_query

class Command(BaseCommand):
    help = 'Executes Sorare API query to find the floor price for all scouting results'

    def handle(self, *args, **options):
        url = "https://api.sorare.com/graphql/"

        scouting_results = ScoutingResult.objects.filter(not_for_sale=False)

        for s in scouting_results:
            # Query the current market offers
            price_query = best_price_query % (s.playerSlug, "limited")

            # Send the request and get the response
            response = requests.post(url, json={"query": price_query}, headers={
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
                floor_price = {
                    "scouting_result": s,
                    "floorPriceETH": min_price / 1000000000000000000.0,
                    "not_for_sale": False,
                }
            except:
                floor_price = {
                    "scouting_result": s,
                    "floorPriceETH": 0,
                    "not_for_sale": True,
                }

            # Get current ETH exchange rate and calculate EUR value
            coinbase_url = "https://api.coinbase.com/v2/exchange-rates?currency=ETH"
            response = requests.get(coinbase_url)
            ETH_EUR = float(json.loads(response.text)["data"]["rates"]["EUR"])
            floor_price["floorPriceEUR"] = floor_price["floorPriceETH"] * ETH_EUR

            FloorPrice.objects.create(
                scouting_result=floor_price["scouting_result"],
                floorPriceETH=floor_price["floorPriceETH"],
                not_for_sale=floor_price["not_for_sale"],
                floorPriceEUR=floor_price["floorPriceEUR"],
            )

