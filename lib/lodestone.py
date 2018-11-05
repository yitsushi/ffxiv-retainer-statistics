import requests
from bs4 import BeautifulSoup
from .item import Item

class Lodestone:
  __character = None
  __session = None

  def __init__(self, character, session):
    self.__character = character
    self.__session = session

  def download(self, retainer):
    headers = {
      'Cookie': f'ldst_touchstone=1; ldst_is_support_browser=1; ldst_cookiepolicy_show=^[^%^22cookiepolicy^%^22^]; ldst_sess={self.__session}'
    }
    url = f'https://eu.finalfantasyxiv.com/lodestone/character/{self.__character}/retainer/{retainer}/'
    return requests.get(url, headers=headers).text

  def sales_history(self, retainer):
    content = self.download(retainer=retainer)
    parsed = BeautifulSoup(content, 'html.parser')
    table = parsed.body.find('div', attrs={'name': 'tab__market-logs'})
    rows = table.find_all('li', attrs={'class': 'item-list__list'})
    return [Item(row, self.__character, retainer) for row in rows]

