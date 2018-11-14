import sqlite3, atexit, logging, sys
from .config import Config

config = Config()
logging.basicConfig(filename=f'{config.log_dir()}/price-history.log', level=logging.INFO)

class Database:
  __connection = None
  __cursor = None

  def __init__(self, path=None):
    if path is None:
      path = f'{config.data_dir()}/retainers.db'
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

    try:
       self.__cursor.execute(
         '''create table items (
              prim text primary key,
              id text,
              job text,
              recipe_id text,
              level integer,
              name text,
              quantity integer,
              durability integer,
              difficulty integer,
              max_quality integer
         )''')
    except:
      pass

    try:
       self.__cursor.execute(
         '''create table ingredients (
              recipe_id text,
              item_id text,
              quantity integer
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
      logging.info(f"added: {item.name} x {item.quantity}")
    except sqlite3.IntegrityError:
      pass
    except Exception as e:
      logging.info(f"skip:  {item.name}x{item.quantity} -> {e}")

  def save_recipe(self, item):
    try:
      self.__cursor.execute('BEGIN TRANSACTION;')
      self.__cursor.execute(
        '''insert into items
            (prim, id, job, recipe_id, level, name, quantity, durability, difficulty, max_quality)
            values(
              ?, ?, ?, ?, ?, ?, ?, ?, ?, ?
            );
        ''',
        [
          f'{item.id}-{item.recipe_id}',
          item.id, item.job, item.recipe_id,
          item.level, item.name,
          item.properties['quantity'],
          item.properties['durability'],
          item.properties['difficulty'],
          item.properties['max_quality']
        ] 
      )

      for id in item.ingredients:
        self.__cursor.execute('''
          insert into ingredients (recipe_id, item_id, quantity)
          values (?, ?, ?);
        ''', [item.recipe_id, id, item.ingredients[id]])

      self.__cursor.execute('COMMIT;')
      #print('.')
    except sqlite3.IntegrityError as e:
      self.__cursor.execute('ROLLBACK;')
      print(f'X -> {e}')
      pass
    except Exception as e:
      self.__cursor.execute('ROLLBACK;')
      print(f"error:  {item.name} -> {e}")

    sys.stdout.flush()

  def execute(self, query):
    self.__cursor.execute(query)
    for line in self.__cursor.fetchall():
      yield line

  def recipe_exists(self, id, job):
    self.__cursor.execute('''
      select 1 from items where recipe_id = ? and job = ?
    ''', [id, job])
    return len(self.__cursor.fetchall()) > 0

  def close(self):
    self.__connection.commit()
    self.__connection.close()

