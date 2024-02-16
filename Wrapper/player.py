'''
Imports
'''
import requests
import datetime
from typing import Union
from json import load

'''
Error Imports
'''
from Exception import RateLimit
from Exception import PlayerNotFound
from Exception import InvalidAPI

class player():
    def __init__(self , userName : str) -> None:
        self.session = requests.session()
        self.userName = userName

        self.playerSearchAPI = load(open('Wrapper/endpoints.json', 'r'))['playerDetails'][0] + str(self.userName)
        self.playerDetailsAPI = load(open('Wrapper/endpoints.json', 'r'))['playerDetails'][1] + str(self.fetchUserId())
        self.playerAssetsAPI = load(open('Wrapper/endpoints.json', 'r'))['playerDetails'][2] + str(self.fetchUserId())

        self.playerId = self.fetchUserId()
        self.cachedInformation = self.cacheUserInformation()

        self.rap = self.cachedInformation['rap']
        self.value = self.cachedInformation['value']
        self.rank = self.cachedInformation['rank']
        self.terminated = self.cachedInformation['terminated']
        self.lastLocation = self.cachedInformation['last_location']

        self.statsUpdated = datetime.datetime.utcfromtimestamp(self.cachedInformation['stats_updated'])
        self.lastUpdated = datetime.datetime.utcfromtimestamp(self.cachedInformation['last_scan'])
        self.lastOnline = datetime.datetime.utcfromtimestamp(self.cachedInformation['last_online'])


    def fetchUserId(self) -> dict | Exception:
        searchedPlayers = self.session.get(self.playerSearchAPI)
        if searchedPlayers.status_code in [200 , 201 , 204]:
            if int(searchedPlayers.json()['result_count']) > 0:
                return searchedPlayers.json()['players'][0][0]
            else:
                raise PlayerNotFound('Player Not Found')
            
        elif searchedPlayers.status_code == 429:
            raise RateLimit('Rate limit has been exceeded')
        
        elif searchedPlayers.status_code in [400 , 404]:
            raise PlayerNotFound('Player Not Found')
        
    def cacheUserInformation(self) -> dict | Exception:
        playerInfo = self.session.get(self.playerDetailsAPI)
        if playerInfo.status_code in [200 , 201 , 204]:
            if playerInfo.json()['success'] == True:
                return playerInfo.json()
            else:
                raise PlayerNotFound('Player Not Found')
            
        elif playerInfo.status_code == 429:
            raise RateLimit('Rate limit has been exceeded')
        
        elif playerInfo.status_code in [400 , 404]:
            raise PlayerNotFound('Player Not Found')
