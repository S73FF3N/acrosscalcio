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
        "LA_LIGA": '["barcelona-barcelona","real-madrid-madrid","real-sociedad-donostia-san-sebastian",\
                   "atletico-madrid-madrid","villarreal-villarreal","real-betis-sevilla",\
                   "rayo-vallecano-madrid","osasuna-pamplona-irunea","athletic-club-bilbao",\
                   "mallorca-palma-de-mallorca","almeria-almeria","girona-girona",\
                   "sevilla-sevilla-1890","valencia-valencia","espanyol-barcelona",\
                   "celta-de-vigo-vigo","real-valladolid-valladolid","cadiz-cadiz",\
                   "getafe-getafe-madrid","elche-elche"]',
    }

scouting_query = '''\
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
    '''
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
    '''