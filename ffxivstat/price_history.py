from ffxivstat.lib import Config
from ffxivstat.lib import Database
from ffxivstat.lib import Lodestone


def run():
    db = Database()
    config = Config()
    ls = Lodestone(config.character(), config.session_id())

    for retainer in config.retainer_ids():
      history = ls.sales_history(retainer=retainer)
      for item in history:
        db.add_sold_item(item)
