from dataclasses import dataclass
import requests
import json

@dataclass
class ZillowSearch():
    def __init__(self, headers: dict):
        self.headers = headers
    
    def findAllHouseData(self, state: str, pages: int) -> list[dict]:
        houseArray = []
        
        for page in range(pages):
            url = 'https://www.zillow.com/search/GetSearchPageState.htm?searchQueryState={"pagination":{"currentPage":' + str(page + 1) +'},"mapBounds":{"west":-109.060256,"east":-102.040878,"south":36.992424,"north":41.003444},"regionSelection":[{"regionId":10,"regionType":2}],"isMapVisible":false,"filterState":{"isAllHomes":{"value":true},"sortSelection":{"value":"days"}},"isListVisible":true}&wants={"cat1":["listResults"],"cat2":["total"]}&requestId=2'
            response = requests.get(url, headers=self.headers)
            houseArray.extend(json.loads(response.content)["cat1"]["searchResults"]["listResults"])
        
        return houseArray
    
    def findAllHousePrices(self, state: str=None) -> list[int]:
        # response = requests.get('https://www.zillow.com/search/GetSearchPageState.htm?searchQueryState={"pagination":{"currentPage":3},"mapBounds":{"west":-109.060256,"east":-102.040878,"south":36.992424,"north":41.003444},"regionSelection":[{"regionId":10,"regionType":2}],"isMapVisible":false,"filterState":{"isAllHomes":{"value":true},"sortSelection":{"value":"days"}},"isListVisible":true}&wants={"cat1":["listResults"],"cat2":["total"]}&requestId=2', headers=self.headers)
        #                          https://www.zillow.com/search/GetSearchPageState.htm?searchQueryState={"pagination":{"currentPage":2},"usersSearchTerm":"Denver, CO","mapBounds":{"west":-105.109927,"east":-104.600296,"south":39.614431,"north":39.914247},"regionSelection":[{"regionId":11093,"regionType":6}],"isMapVisible":false,"filterState":{"sortSelection":{"value":"days"},"isAllHomes":{"value":true}},"isListVisible":true}&wants={"cat1":["listResults"],"cat2":["total"]}&requestId=2
        raise NotImplementedError()

def main(headers):
    houseSearch = ZillowSearch(headers)
    houseArray = houseSearch.findAllHouseData("Colorado", 2)

    for house in houseArray:
            print("--------------------------------------\n"
                  f"Price : {house['price']}\n"
                  f"Status Text : {house['statusText']}\n"
                  f"Status Type : {house['statusType']}\n"
                  f"Beds : {house['beds']}\n"
                  f"Baths : {house['baths']}\n"
                  f"State : {house['addressState']}\n"
                  f"City : {house['addressCity']}\n"
                  f"Street : {house['addressStreet']}\n"
                  f"ZipCode : {house['addressZipcode']}")

if __name__ == '__main__':
    with open("./json/headers.json", "r") as headersJSON:
        headers = json.load(headersJSON)
    
    main(headers)
