''''
Imports
'''
import requests
from typing import Optional , Union


'''
Rolimons Items Details Class
'''
class RolimonsItemDetails():
    def __init__(self) -> None:
        self.itemAPI = 'https://api.rolimons.com/items/v1/itemdetails'
        self.responseCodes = [200 , 201 , 204]

    def fetchItemData(self, itemId: Union[str, int]) -> Optional[dict]:
        """
        Fetches and returns a dictionary containing details of a Roblox item.
        Returns None if the item is not found or if there's an API error.
        """
        params = {
            'item_id': itemId
            }
        
        response = requests.get(self.itemAPI , params = params)
        if response.status_code in self.responseCodes:
            try:
                data = response.json()
                if data['success'] and str(itemId) in data['items']:
                    itemDetails = data['items'][str(itemId)]
                    return {
                        'itemName': itemDetails[0],
                        'itemAcronym': itemDetails[1],
                        'itemValue': itemDetails[2]
                    }
                else:
                    return None
            except KeyError:
                return None
        else:
            return None
            

itemJson = RolimonsItemDetails().fetchItemData(11748356)
if itemJson:
    print('Item Details:: %s' % str(itemJson))
else:
    print('Item not found or API error')