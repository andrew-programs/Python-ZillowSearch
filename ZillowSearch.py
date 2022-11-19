from dataclasses import dataclass
import requests # Not std
import json
import csv

class ZillowSearch():
    def gatherHouseData(self, state: str, pages: int, headers: dict, output: bool=False) -> list[dict]:
        """This method will gather data from Zillow and return a list of dictionaries"""
        # NOTE : Add kwargs or args option to make calling the method easier.
        houseArray = []
        
        for page in range(pages):
            url = 'https://www.zillow.com/search/GetSearchPageState.htm?searchQueryState={"pagination":{"currentPage":' + str(page + 1) +'},"mapBounds":{"west":-109.060256,"east":-102.040878,"south":36.992424,"north":41.003444},"regionSelection":[{"regionId":10,"regionType":2}],"isMapVisible":false,"filterState":{"isAllHomes":{"value":true},"sortSelection":{"value":"days"}},"isListVisible":true}&wants={"cat1":["listResults"],"cat2":["total"]}&requestId=2'
            response = requests.get(url, headers=headers)
            houseArray.extend(json.loads(response.content)["cat1"]["searchResults"]["listResults"])
        
        # NOTE : Example of practical kwarg or arg.
        if output == True:
            headerRow = ["Price", "Status Text", "Status Type", "Area", "Beds", "Baths", "State", "City", "Street", "Zipcode"]
            
            with open("./output/ZillowHouses.CSV", "w") as dataFile:
                csvWriter = csv.writer(dataFile)
                csvWriter.writerow(headerRow)
                
                for house in houseArray:
                    csvWriter.writerow(["{:,}".format(house['unformattedPrice']), house['statusType'], house['statusType'], f"{house['area']} sqft", house['beds'], house['baths'], house['addressState'], house['addressCity'], house['addressStreet'], house['addressZipcode']])
                
        return houseArray
    
    def findAllHousePrices(self, state: str=None) -> list[int]:
        """Not implemented"""
        raise NotImplementedError()

# main test function
def main(headers):
    houseSearch = ZillowSearch()
    houseArray = houseSearch.gatherHouseData("Colorado", 5, headers, True)
    print(houseArray)

if __name__ == '__main__':
    with open("./json/headers.json", "r") as headersJSON:
        headers = json.load(headersJSON)
    
    main(headers)
