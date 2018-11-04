#!/usr/bin/env python

import requests, hashlib, sqlite3, atexit, os
from bs4 import BeautifulSoup

character = '14867589'

retainers = [
        'f49f0239a5', # Lominsaret
        'ad32977801', # Chimomo
        '6f49aebcb1', # Liwita
        'f2d1754992', # Chookity
]

class Item:
    id = None
    name = None
    quantity = None
    isHQ = False
    price = None
    date = None
    buyer = None
    retainer = None
    character = None

    def __init__(self, row, character, retainer):
        self.character = character
        self.retainer = retainer

        name = row.find('p', attrs={'class': 'item-list__name'})
        img = name.find('img')
        self.isHQ = (img is not None)
        (self.name, self.quantity) = [n.strip('()\t ') for n in name.text.strip().split('\n') if n.strip() != '']
        self.quantity = int(self.quantity)

        self.price = int(row.find('div', attrs={'class': 'item-list__item item-list__cell--sm'}).text.replace(',', ''))
        self.date = int(row.find('span')['data-epoch'])
        self.buyer = row.find('div', attrs={'class': 'item-list__item item-list__cell--md'}).text

        base = f'{self.name}|{self.buyer}'
        self.id = "{0}{1}".format(hashlib.sha256(base.encode()).hexdigest(), self.date)

    def to_array(self):
      return [
        self.id, self.name, self.quantity, self.isHQ,
        self.price, self.date, self.buyer,
        self.retainer, self.character
      ]

class Database:
  __connection = None
  __cursor = None

  def __init__(self, path='retainers.db'):
    atexit.register(self.close)
    self.__connection = sqlite3.connect(path)
    self.__cursor = self.__connection.cursor()
    self.__create_tables()

  def __create_tables(self):
    try:
       self.__cursor.execute(
         '''create table sales_history (
              id text primary key,
              name text,
              quantity integer,
              isHQ integer,
              price real,
              date real,
              buyer text,
              retainer text,
              character text
         )''')
    except:
      pass

  def add_sold_item(self, item):
    try:
      self.__cursor.execute(
        '''insert into sales_history
             (id, name, quantity, isHQ, price, date, buyer, retainer, character)
             values (
               ?, ?, ?, ?, ?, ?, ?, ?, ?
        )''',
        item.to_array()
      )
      self.__connection.commit()
      print(f"added: {item.name}x{item.quantity}")
    except Exception as e:
      pass
      print(f"skip:  {item.name}x{item.quantity}")

  def close(self):
    self.__connection.commit()
    self.__connection.close()


def download(*, character, retainer):
  headers = {
    'Cookie': f'ldst_touchstone=1; ldst_is_support_browser=1; ldst_cookiepolicy_show=^[^%^22cookiepolicy^%^22^]; ldst_sess={os.getenv("SESSION_ID")}'
  }
  url = f'https://eu.finalfantasyxiv.com/lodestone/character/{character}/retainer/{retainer}/'
  return requests.get(url, headers=headers).text

def sales_history(*, character, retainer):
  content = download(character=character, retainer=retainer)
  parsed = BeautifulSoup(content, 'html.parser')
  table = parsed.body.find('div', attrs={'name': 'tab__market-logs'})
  rows = table.find_all('li', attrs={'class': 'item-list__list'})
  return [Item(row, character, retainer) for row in rows]
    
db = Database()

for retainer in retainers:
  history = sales_history(character=character, retainer=retainer)
  for item in history:
    db.add_sold_item(item)
