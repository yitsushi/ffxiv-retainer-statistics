# FFXIV Retainer Statistics

## Config

Example:

```
# ~/.config/ffxiv/app.yaml
---
session: "ldst_sess from cookies from lodestone"
character: "your-character-id"
retainers:
  f49f0239a5: Lominsaret
  ad32977801: Chimomo
  6f49aebcb1: Liwita
  f2d1754992: Chookity
log_directory: /home/yourusername/.data/ffixv/yourcharacter/log
data_directory: /home/yourusername/.data/ffixv/yourcharacter/data
sendgrid:
  id: api-id
  token: api-token
  from:
    email: no-reply@from-email-address
    name: FFXIV Retainer Statistics System
  to:
   - email: your.email@address
     name: Your Name
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

  * use per character config files: ~/.config/ffxiv/charactername.yaml
  * specify `RETAINER_CONFIG` environment variable

## Commands

```
craftable-gatherable-items      downloads craftable and gatherable items/recipes
direct-items                    downloads items for craftable items (not listed as craftable)
email-report                    send an email about your income
find                            find a recipe
price-history                   downloads your sold items history
report                          generates a report about your retainers / income
```

### find

```
> ./find "Tigerskin Tricorne of Striking"
  1x [LTW::65] Tigerskin Tricorne of Striking
      2x [LTW::64] Tiger Leather
          6x [None::None] Tiger Skin
          2x [MIN_mining::60] Gyr Abanian Alumen
          8x [MIN_quarrying::26] Earth Crystal
      1x [GSM::64] Durium Nugget
          4x [MIN_quarrying::66] Durium Sand
          1x [MIN_mining::25] Silver Ore
          4x [MIN_quarrying::26] Wind Crystal
      1x [GSM::62] Koppranickel Ingot
          4x [MIN_mining::63] Koppranickel Ore
          1x [GSM::61] Koppranickel Nugget
              4x [MIN_quarrying::61] Koppranickel Sand
              1x [MIN_mining::1] Copper Ore
              3x [MIN_quarrying::26] Wind Crystal
          3x [MIN_quarrying::26] Wind Crystal
      1x [WVR::62] Ruby Cotton Yarn
          4x [BTN_harvesting::63] Ruby Cotton Boll
          3x [MIN_quarrying::26] Lightning Crystal
      1x [ALC::63] Grade 1 Reisui of Strength
          1x [MIN_mining::61] Gyr Abanian Mineral Water
          2x [BTN_harvesting::63] Holy Basil
          2x [BTN_harvesting::58] Rue
          1x [MIN_quarrying::63] Diatomite
          4x [MIN_quarrying::26] Water Crystal
      4x [MIN_quarrying::26] Earth Crystal
      4x [MIN_quarrying::26] Wind Crystal
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

@hourly    RETAINER_CONFIG=~/.config/ffxiv/charactername.yaml /path/to/the/repo//ffxiv-retainer-statistics/price-history
@daily     RETAINER_CONFIG=~/.config/ffxiv/charactername.yaml /path/to/the/repo/ffxiv-retainer-statistics/email-report
```
