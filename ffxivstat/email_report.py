import sqlite3
from ffxivstat.lib import Config
from ffxivstat.lib import Database
from ffxivstat.lib import SendGrid
from ffxivstat.lib import MailGun

config = Config()
db = Database()

def section(*, output, title, query):
    output.append('')
    output.append(f'# {title}')
    output.append('')

    for line in db.execute(query):
      yield line

    output.append('')

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
    generated_lines = []

    for line in section(output=generated_lines, title='Daily Income', query=queries['daily']):
        generated_lines.append('  {0:12s}{1:10,} g'.format(line[0], round(line[1])))

    for line in section(output=generated_lines, title='Last Three Days Leaderboard', query=queries['leaderboard']):
        generated_lines.append('  {0:12s}{1:10,} g'.format(config.retainer(line[0]), round(line[1])))

    for line in section(output=generated_lines, title='Top 5 Products (per item) in the last 5 days (Avg price)', query=queries['uniq_price']):
        generated_lines.append('  {2} {0:40s}{1:10,} g'.format(line[0], round(line[1]), '*' if line[2] == 1 else ' '))

    for line in section(output=generated_lines, title='Top 5 Bulk Products in the last 5 days (Avg price)', query=queries['sum_price']):
        generated_lines.append('  {2} {0:40s}{1:10,} g'.format(line[0], round(line[1]), '*' if line[2] == 1 else ' ', line[3]))

    for line in section(output=generated_lines, title='Last N items', query=queries['lastN']):
        generated_lines.append(' [{4:s}] {3:2d}x {2} {0:40s}{1:10,} g'.format(line[0], round(line[1]), '*' if line[2] == 1 else ' ', line[3], line[4]))

    text = "\n".join(generated_lines)
    html = f'''
<html>
<body>
<pre>
{text}
</pre>
</body>
</html>'''
    MailGun().send(text, html)
