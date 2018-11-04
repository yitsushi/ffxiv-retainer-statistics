#!/usr/bin/env python

import sqlite3

print('# Daily income:')
print('')
query = '''select date(date, 'unixepoch'), sum(price) from sales_history group by date(date, 'unixepoch') order by date desc;'''

connection = sqlite3.connect('retainers.db')
cursor = connection.cursor()
cursor.execute(query)
for line in cursor.fetchall():
    print('  {0:12s}{1:15,} g'.format(line[0], round(line[1])))


retainers = {
        'f49f0239a5': 'Lominsaret',
        'ad32977801': 'Chimomo',
        '6f49aebcb1': 'Liwita',
        'f2d1754992': 'Chookity',
}

print('')

print('# Last 3 days leaderboard:')
print('')
query = '''select retainer, sum(price) from sales_history where date(date, 'unixepoch') > date('now', '-3 day') group by retainer order by sum(price) desc;'''

connection = sqlite3.connect('retainers.db')
cursor = connection.cursor()
cursor.execute(query)
for line in cursor.fetchall():
    print('  {0:12s}{1:15,} g'.format(retainers[line[0]], round(line[1])))
