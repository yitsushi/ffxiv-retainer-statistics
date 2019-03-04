import sqlite3
from ffxivstat.lib import Config
from ffxivstat.lib import reporter
from ffxivstat.lib.database import SalesHistory


def run():
    config = Config()
    for line in reporter.section(title='Daily Income (7 days)',
                                 character=config.character(),
                                 function=reporter.daily_income,
                                 days=7):
        print('  {0:12s}{1:10,} g'.format(str(line[0]), line[1]))

    for line in reporter.section(title='Last Three Days Leaderboard',
                                 character=config.character(),
                                 function=reporter.retainer_leaderboard,
                                 days=3):
        print('  {0:12s}{1:10,} g'.format(config.retainer(line[0]), line[1]))

    for line in reporter.section(
            title='Top 5 Products (per item) in the last 5 days (Avg price)',
            character=config.character(),
            function=reporter.top_products,
            days=5,
            limit=5):
        print(
            '  {2} {0:40s}{1:10,} g'.format(
                line[0],
                round(
                    line[1]),
                '*' if line[2] == 1 else ' '))

    for line in reporter.section(
            title='Top 5 Bulk Products in the last 5 days (Avg price)',
            character=config.character(),
            function=reporter.top_bulk_products,
            days=5,
            limit=5):
        print(
            '  {2} {0:40s}{1:10,} g'.format(
                line[0],
                round(
                    line[1]),
                '*' if line[2] == 1 else ' ',
                line[3]))

    for line in reporter.section(title='Last N items',
                                 character=config.character(),
                                 function=reporter.last,
                                 limit=10):
        print(' [{4:s}] {3:2d}x {2} {0:40s}{1:10,} g'.format(
            line[0], line[1], '*' if line[2] == 1 else ' ', line[3], str(line[4])))
