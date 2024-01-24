''''
Imports
'''
import requests
from typing import Optional , Union

'''
Error Imports
'''
from .errorException import RateLimit
from .errorException import ItemNotFound
from .errorException import InvalidAPI


'''
Rolimons Items Class
'''
class RolimonsItems():
    def __init__(self) -> None:
        self.session = requests.Session()
        self.itemAPI = 'https://api.rolimons.com/items/v1/itemdetails'
        self.itemsCache = self.fetchAllItems()


    def fetchAllItems(self) -> dict:
        '''
        Fetches and caches all item data from the API.
        '''
        response = self.session.get(self.itemAPI)
        if response.status_code in [200 , 201 , 204]:
            try:
                roliData = response.json()
                if 'success' in roliData and roliData['success']:
                    return roliData['items'] if 'items' in roliData else {}
                else:
                    raise InvalidAPI('Invalid API')
            except KeyError:
                raise InvalidAPI('Invalid API')
        elif response.status_code == 429:
            raise RateLimit('Rate limit has been exceeded')
        else:
            raise InvalidAPI('API error %s' % response.text())

    def ItemInfo(self, searchValue: Union[str, int]) -> Optional[str]:
        """
        Fetches item information by item ID, acronym, or name.
        """
        searchValueStr = str(searchValue).lower()
        for itemId, details in self.itemsCache.items():
            detailsStr = [str(detail).lower() for detail in details]
            if searchValueStr in detailsStr:
                return ('Item Name: %s, Acronym: %s, RAP: %s, Value: %s, ' 'Default Value: %s, Demand: %s, Trend: %s, ' 'Projected: %s, Hyped: %s, Rare: %s' % tuple(details))
        raise ItemNotFound('Item not found: %s' % searchValue)
