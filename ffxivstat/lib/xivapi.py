import requests
import re
import json

class XIVAPI:
    __key = None
    __market = None

    def __init__(self, api_key, market):
        self.__key = api_key
        self.__market = market

    def download(self, path):
        url = f'https://eu.finalfantasyxiv.com/lodestone{path}'
        return requests.get(url, headers=headers).text

    def find(self, kwd):
        query = {
            "indexes":  "item",
            "filters":  "ItemSearchCategory.ID>=1",
            "columns":  "ID,Name",
            "string":   kwd,
            "limit":    50,
            "key":      self.__key,
            "language": "en"
        }
        url = 'https://xivapi.com/search'
        response = requests.get(url, query).text
        return json.loads(response)['Results']

    def find_exact(self, name):
        items = self.find(name)
        match = [x for x in items if x['Name'] == name]
        if len(match) < 1:
            return None
        return match[0]

    def price(self, name):
        item = self.find_exact(name)
        if item is None:
            return None

        query = {
            'key': self.__key,
            'language': 'en'
        }
        url = f"https://xivapi.com/market/{self.__market}/items/{item['ID']}"
        prices = json.loads(requests.get(url, query).text)['Prices']

        hq = [x['PricePerUnit'] for x in prices if x['IsHQ']]
        nq = [x['PricePerUnit'] for x in prices if not x['IsHQ']]

        if len(hq) < 1:
            hq = [0]
        if len(nq) < 1:
            nq = [0]

        return {
            'nq': {'min': min(nq), 'max': max(nq)},
            'hq': {'min': min(hq), 'max': max(hq)}
        }
