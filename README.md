# FFXIV Retainer Statistics

## Config

Example:

```
# ~/.config//app.yaml
---
session: "ldst_sess from cookies from lodestone"
character: "your-character-id"
retainers:
  f49f0239a5: Lominsaret
  ad32977801: Chimomo
  6f49aebcb1: Liwita
  f2d1754992: Chookity
data_directory: /home/yourusername/.data/ffixv/yourcharacter/data
database:
  type: postgres
  host: hostname
  port: 5432
  user: username
  password: password
database:
mailgun:
  domain: your domain
  api_key: api-key
  from:
    email: no-reply@from-email-address
    name: FFXIV Retainer Statistics System
  to:
   - email: your.email@address
     name: Your Name
```

If you want to use more than one account:

  * use per character config files: ~/.config//charactername.yaml
  * specify `RETAINER_CONFIG` environment variable

## Commands

```
email-report                    send an email about your income
price-history                   downloads your sold items history
report                          generates a report about your retainers / income
```


### report

```
> ./report
# Daily Income (7 days)

  2018-11-12   3,164,075 g
  2018-11-11   4,879,120 g
  2018-11-10  11,663,900 g
  2018-11-09   5,583,625 g
  2018-11-08   1,065,900 g
  2018-11-07   1,411,035 g
  2018-11-06     244,380 g


# Last Three Days Leaderboard

  Liwita       2,953,650 g
  Chookity       169,100 g
  Chimomo         41,325 g


# Top 5 Products (per item) in the last 5 days (Avg price)

    Modern Aesthetics - Form and Function    2,813,000 g
    Mitigative Logogram                        817,000 g
    Protective Logogram                        611,625 g
    Tactical Logogram                          298,775 g
  * Mythrite Bangle of Casting                  85,500 g


# Top 5 Bulk Products in the last 5 days (Avg price)

    Mitigative Logogram                        817,000 g
    Protective Logogram                        722,225 g
    Tactical Logogram                          298,775 g
    Curative Logogram                           85,500 g
    Fundamental Logogram                        47,500 g


# Last N items

 [2018-11-12 21:59:29] 37x   Gagana Egg                                  17,575 g
 [2018-11-12 21:49:39]  1x   Fundamental Logogram                        28,500 g
 [2018-11-12 21:46:45]  1x   Modern Aesthetics - Form and Function    2,813,000 g
 [2018-11-12 21:41:55]  2x   Heavens' Eye Materia VI                     55,100 g
 [2018-11-12 21:41:39]  2x   Savage Might Materia VI                     38,800 g
```

## Example cron

```
HOME=/home/youruser

@hourly    RETAINER_CONFIG=~/.config//charactername.yaml /path/to/the/repo//-retainer-statistics/price-history
@daily     RETAINER_CONFIG=~/.config//charactername.yaml /path/to/the/repo/-retainer-statistics/email-report
```

## Extra

It uses a simple sqlite database, so you can make your extra tools like based on Pyros,
check your income from Logograms a simple Bash script looks like this:

```
#!/bin/bash

sqlite3 ~/.data/ffixv/charactername/data/retainers.db \
        -line \
        "select name, sum(price), sum(quantity) from sales_history where name like '%logogram%' group by name;"

echo -e "\n === Summary:\n"
sqlite3 ~/.data/ffixv/charactername/data/retainers.db \
        -line \
        "select sum(price), sum(quantity) from sales_history where name like '%logogram%';"
```
