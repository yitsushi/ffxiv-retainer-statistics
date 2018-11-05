import sqlite3, atexit, logging

logging.basicConfig(filename='log/price-history.log', level=logging.INFO)

class Database:
  __connection = None
  __cursor = None

  def __init__(self, path='data/retainers.db'):
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
      logging.info(f"added: {item.name} x {item.quantity}")
    except sqlite3.IntegrityError:
      pass
    except Exception as e:
      logging.info(f"skip:  {item.name}x{item.quantity} -> {e}")

  def execute(self, query):
    self.__cursor.execute(query)
    for line in self.__cursor.fetchall():
      yield line

  def close(self):
    self.__connection.commit()
    self.__connection.close()

