#!/usr/bin/env python

import sqlite3

def section(*, title, query):
    print('')
    print(f'# {title}')
    print('')

    connection = sqlite3.connect('retainers.db')
    cursor = connection.cursor()
    cursor.execute(query)
    for line in cursor.fetchall():
        yield line

    connection.close()
    print('')

queries = {
    'daily': '''select date(date, 'unixepoch'), sum(price)
                    from sales_history
                    group by date(date, 'unixepoch')
                    order by date desc;''',
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
}

retainers = {
        'f49f0239a5': 'Lominsaret',
        'ad32977801': 'Chimomo',
        '6f49aebcb1': 'Liwita',
        'f2d1754992': 'Chookity',
}



for line in section(title='Daily Income', query=queries['daily']):
    print('  {0:12s}{1:15,} g'.format(line[0], round(line[1])))

for line in section(title='Last Three Days Leaderboard', query=queries['leaderboard']):
    print('  {0:12s}{1:15,} g'.format(retainers[line[0]], round(line[1])))

for line in section(title='Top 5 Products (per item) in the last 5 days', query=queries['uniq_price']):
    print('  {2} {0:40s}{1:15,} g'.format(line[0], round(line[1]), '*' if line[2] == 1 else ' '))

for line in section(title='Top 5 Bulk Products in the last 5 days', query=queries['sum_price']):
    print('  {2} {0:40s}{1:10,} g'.format(line[0], round(line[1]), '*' if line[2] == 1 else ' ', line[3]))
