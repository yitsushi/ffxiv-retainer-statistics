from datetime import datetime
from pony import orm
from .config import Config

config = Config()
db = orm.Database()

if config.db_type() == 'postgres':
    details = config.database()
    db.bind(provider='postgres',
            user=details['user'],
            password=details['password'],
            host=details['host'],
            port=details['port'],
            database=details['name'])
else:
    db.bind(provider='sqlite',
            filename=f'{config.data_dir()}/retainers.db',
            create_db=True)

class SalesHistory(db.Entity):
    id = orm.PrimaryKey(str, auto=False)
    name = orm.Required(str)
    quantity = orm.Required(int)
    is_hq = orm.Required(bool)
    price = orm.Required(int)
    date = orm.Required(datetime)
    buyer = orm.Required(str)
    retainer = orm.Required(str)
    character = orm.Required(str)

db.generate_mapping(create_tables=True)

@orm.db_session(sql_debug=False)
def save_new_slaes_history_item(item):
    if SalesHistory.get(id=item.id) is None:
        SalesHistory(id=item.id,
                     character=item.character,
                     retainer=item.retainer,
                     name=item.name,
                     quantity=item.quantity,
                     is_hq=item.is_hq,
                     price=item.price,
                     date=item.date,
                     buyer=item.buyer)

