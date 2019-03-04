from ffxivstat.lib import Config
from ffxivstat.lib import Lodestone
from ffxivstat.lib.database import save_new_slaes_history_item


def run():
    config = Config()
    ls = Lodestone(config.character(), config.session_id())

    for retainer in config.retainer_ids():
        for item in ls.sales_history(retainer=retainer):
            save_new_slaes_history_item(item)

