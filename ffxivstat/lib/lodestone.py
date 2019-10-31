import hashlib
import re
import requests
from bs4 import BeautifulSoup
from collections import namedtuple
from datetime import datetime
from .database import SalesHistory


SalesHistoryItem = namedtuple('SalesHistoryItem',
                              ('id', 'character', 'retainer',
                               'name', 'quantity', 'is_hq',
                               'price', 'date', 'buyer'))

def u2d(t):
    '''Unix Timestamp to DateTime'''
    return datetime.utcfromtimestamp(t)

class Lodestone:
  __character = None
  __session = None

  def __init__(self, character, session):
    self.__character = character
    self.__session = session

  def download(self, path):
    cookies = [
      'ldst_touchstone=1',
      'ldst_is_support_browser=1',
      'ldst_cookiepolicy_show=^[^%^22cookiepolicy^%^22^]',
      f'ldst_sess={self.__session}'
    ]
    headers = {
      'Cookie': '; '.join(cookies)
    }
    url = f'https://eu.finalfantasyxiv.com/lodestone{path}'
    return requests.get(url, headers=headers).text

  def sales_history(self, retainer):
    content = self.download(f'/character/{self.__character}/retainer/{retainer}/')
    parsed = BeautifulSoup(content, 'html.parser')
    table = parsed.body.find('div', attrs={'name': 'tab__market-logs'})
    rows = table.find_all('li', attrs={'class': 'item-list__list'})

    for row in rows:
        name_tag = row.find('p', attrs={'class': 'item-list__name'})
        is_hq = False
        # img = name_tag.find('img')
        # is_hq = (img is not None)
        name = name_tag.text.strip()
        quantity = int(re.search(r'\((\d+)\)', name).group(1))
        if '\ue03c' in name:
            is_hq = True
        name = name[:-(len(str(quantity)) + 2)]
        name = name.replace('\ue03c', '')

        price = int(row.find('div', attrs={'class': 'item-list__item item-list__cell--sm'}).text.replace(',', ''))
        date = int(row.find('span', attrs={'class': 'datetime_dynamic_ymdhm'})['data-epoch'])
        buyer = row.find('div', attrs={'class': 'item-list__item item-list__cell--md'}).text

        base = f'{name}|{buyer}'
        _id = "{0}{1}".format(hashlib.sha256(base.encode()).hexdigest(), date)

        yield SalesHistoryItem(id=_id,
                               character=self.__character,
                               retainer=retainer,
                               name=name,
                               quantity=quantity,
                               is_hq=is_hq,
                               price=price,
                               date=u2d(date),
                               buyer=buyer)

