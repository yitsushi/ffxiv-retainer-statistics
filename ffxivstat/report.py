import sqlite3
from ffxivstat.lib import Database
from ffxivstat.lib import Config

config = Config()
db = Database()

def section(*, title, query):
    print('')
    print(f'# {title}')
    print('')

    for line in db.execute(query):
      yield line

    print('')

queries = {
    'daily': '''select date(date, 'unixepoch'), sum(price)
                    from sales_history
                    group by date(date, 'unixepoch')
                    order by date desc
                    limit 7;''',
    'leaderboard': '''select retainer, sum(price)
                    from sales_history
                    where date(date, 'unixepoch') > date('now', '-3 day')
                    group by retainer
                    order by sum(price) desc;''',
    'uniq_price': '''select name, avg(price/quantity), ishq
                    from sales_history
                    where date(date, 'unixepoch') > date('now', '-5 day')
                    group by name, ishq
                    order by avg(price/quantity) desc
                    limit 5;''',
    'sum_price': '''select name, avg(price/quantity), ishq, quantity
                    from sales_history
                    where date(date, 'unixepoch') > date('now', '-5 day') and quantity > 1
                    group by name, ishq
                    order by avg(price/quantity) desc
                    limit 5;''',
    'lastN': '''select name, price, ishq, quantity, datetime(date, 'unixepoch')
                    from sales_history
                    order by date desc
                    limit 10;''',
}

def run():
    for line in section(title='Daily Income (7 days)', query=queries['daily']):
        print('  {0:12s}{1:10,} g'.format(line[0], round(line[1])))

    for line in section(title='Last Three Days Leaderboard', query=queries['leaderboard']):
        print('  {0:12s}{1:10,} g'.format(config.retainer(line[0]), round(line[1])))

    for line in section(title='Top 5 Products (per item) in the last 5 days (Avg price)', query=queries['uniq_price']):
        print('  {2} {0:40s}{1:10,} g'.format(line[0], round(line[1]), '*' if line[2] == 1 else ' '))

    for line in section(title='Top 5 Bulk Products in the last 5 days (Avg price)', query=queries['sum_price']):
        print('  {2} {0:40s}{1:10,} g'.format(line[0], round(line[1]), '*' if line[2] == 1 else ' ', line[3]))

    for line in section(title='Last N items', query=queries['lastN']):
        print(' [{4:s}] {3:2d}x {2} {0:40s}{1:10,} g'.format(line[0], round(line[1]), '*' if line[2] == 1 else ' ', line[3], line[4]))
