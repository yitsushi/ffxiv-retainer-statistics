import requests
from bs4 import BeautifulSoup
from .sellitem import SellItem
from .onsaleitem import OnSaleItem
from .item import Item
import re

class Lodestone:
  __character = None
  __session = None

  __labels = {
    'Total Crafted': ('quantity', lambda x: int(x)),
    'Durability': ('durability', lambda x: int(x)),
    'Difficulty': ('difficulty', lambda x: int(x)),
    'Maximum Quality': ('max_quality', lambda x: int(x))
  }

  crafter_jobs = [
    'CRP', 'BSM', 'ARM', 'GSM',
    'LTW', 'WVR', 'ALC', 'CUL'
  ]

  gatherer_jobs = [
    'MIN_mining', 'MIN_quarrying',
    'BTN_logging', 'BTN_harvesting'
  ]

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
    return [SellItem(row, self.__character, retainer) for row in rows]

  def download_gathering(self, gathering_id):
    item = Item()

    content = self.download(f'/playguide/db/gathering/{gathering_id}/')
    parsed = BeautifulSoup(content, 'html.parser').body.find('div', attrs={'class': 'db_cnts'})

    link = parsed.find('div', attrs={'class': 'db-tooltip__bt_item_detail'}).find('a')['href']

    item.id = re.search(r'db/item/([0-9a-z]+)/', link).group(1)
    item.level = parsed.find('span', attrs={'class': 'db-view__item__text__level__num'}).text

    return item

  def download_recipe(self, recipe_id):
    item = Item()

    content = self.download(f'/playguide/db/recipe/{recipe_id}/')
    parsed = BeautifulSoup(content, 'html.parser').body.find('div', attrs={'class': 'recipe_detail item_detail_box'})

    link = parsed.find('div', attrs={'class': 'db-tooltip__bt_item_detail'}).find('a')['href']

    item.id = re.search(r'db/item/([0-9a-z]+)/', link).group(1)
    item.level = parsed.find('span', attrs={'class': 'db-view__item__text__level__num'}).text

    items = parsed.find_all('div', attrs={'class': 'db-view__data__reward__item__name'})
    for row in items:
      quantity = int(row.find('span', attrs={'class': 'db-view__item_num'}).text)
      r_id = re.search(r'db/item/([0-9a-z]+)/', row.find('a')['href']).group(1)
      item.add_ingredient(r_id, quantity)

    details = parsed.find('ul', attrs={'class': 'db-view__recipe__craftdata'}).find_all('li')
    for prop in details:
      label = prop.find('span').text
      value = prop.find(text=True, recursive=False)
      if label in self.__labels:
        c = self.__labels[label]
        item.set_property(c[0], c[1](value))

    return item

  def gathering_log(self, job, db):
    job_id = self.gatherer_jobs.index(job)
    current_page = 0
    has_next_page = True
    while has_next_page:
      current_page += 1
      print(f"Downloading page #{current_page} or {job}")
      content = self.download(f'/playguide/db/gathering/?category2={job_id}&page={current_page}')
      parsed = BeautifulSoup(content, 'html.parser')
      has_next_page = parsed.body.find('a', attrs={'rel': 'next'}) is not None

      table = parsed.body.find('div', attrs={'class': 'db-table__wrapper'})
      items = table.find_all('a', attrs={'class': 'db_popup db-table__txt--detail_link'})

      for item in items:
        link = item['href']
        gathering_id = re.search(r'gathering/([0-9a-f]+)/', link).group(1)

        if db.recipe_exists(gathering_id, job):
          continue

        name = item.text
        gathering = self.download_gathering(gathering_id)

        gathering.job = job
        gathering.name = name
        gathering.recipe_id = gathering_id

        yield gathering

  def crafting_log(self, job, db):
    job_id = self.crafter_jobs.index(job)
    current_page = 0
    has_next_page = True
    while has_next_page:
      current_page += 1
      print(f"Downloading page #{current_page} or {job}")
      content = self.download(f'/playguide/db/recipe/?category2={job_id}&page={current_page}')
      parsed = BeautifulSoup(content, 'html.parser')
      has_next_page = parsed.body.find('a', attrs={'rel': 'next'}) is not None

      table = parsed.body.find('div', attrs={'class': 'db-table__wrapper'})
      items = table.find_all('a', attrs={'class': 'db_popup db-table__txt--detail_link'})

      for item in items:
        link = item['href']
        recipe_id = re.search(r'recipe/([0-9a-f]+)/', link).group(1)

        if db.recipe_exists(recipe_id, job):
          continue

        name = item.text
        recipe = self.download_recipe(recipe_id)

        recipe.job = job
        recipe.name = name
        recipe.recipe_id = recipe_id

        yield recipe

  def download_item_minimal(self, item_id):
    content = self.download(f'/playguide/db/item/{item_id}/')
    parsed = BeautifulSoup(content, 'html.parser')
    name = parsed.body.find(
            'div',
            attrs={'class': 'db-view__item__text__inner'}
    ).find('h2').find(
            text=True,
            recursive=False
    ).strip()
    item = Item()
    item.name = name
    item.id = item_id
    item.recipe_id = 'None'
    return item

  def on_sale(self, retainer):
    content = self.download(f'/character/{self.__character}/retainer/{retainer}/')
    parsed = BeautifulSoup(content, 'html.parser')
    table = parsed.body.find('div', attrs={'name': 'tab__market-list'})
    rows = table.find_all('li', attrs={'class': 'item-list__list'})
    return [OnSaleItem(row, self.__character, retainer) for row in rows]
