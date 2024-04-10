import random
def getOptions(category,number):
    options=[]
    if category=="Sports":
        options = [
            {'name': 'Football', 'image': 'leagueOfLegends.png','banner':'LoLbanner.png'},
            {'name': 'BasketBall', 'image': 'valorant.png','banner':'ValorantBanner.png'},
            {'name': 'Rugby', 'image': 'CounterStrike.png','banner':'CSGOBanner.png'},
            {'name': 'Golf', 'image': 'RocketLeague.png','banner':'RocketLeagueHeader.png'},
            {'name': 'Baseball', 'image': 'leagueOfLegends.png','banner':'LoLbanner.png'},
            {'name': 'Hockey', 'image': 'valorant.png','banner':'ValorantBanner.png'},
            {'name': 'Tennis', 'image': 'CounterStrike.png','banner':'CSGOBanner.png'},
            {'name': 'VolleyBall', 'image': 'RocketLeague.png','banner':'RocketLeagueHeader.png'},
            {'name': 'Swimming', 'image': 'valorant.png','banner':'ValorantBanner.png'},
            {'name': 'Soccer', 'image': 'CounterStrike.png','banner':'CSGOBanner.png'},
        ]
        options = random.sample(options, number)
        random.shuffle(options)
    else:
        options = [
            {'name': 'League Of Legends', 'image': 'leagueOfLegends.png','banner':'LoLbanner.png'},
            {'name': 'Valorant', 'image': 'valorant.png','banner':'ValorantBanner.png'},
            {'name': 'Counter-Strike', 'image': 'CounterStrike.png','banner':'CSGOBanner.png'},
            {'name': 'Rocket League', 'image': 'RocketLeague.png','banner':'RocketLeagueHeader.png'},
            {'name': 'Fortnite', 'image': 'Fortnite.png','banner':'FortniteBanner.png'}
        ]    
    return options