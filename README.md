# Telegram Weather Bot
This is simply telegram bot, which show current weather in current place.
---
## Bot commands:
- **/place** - Input place.
- **/update** - Update weather of current place.
- **/current_place** - Output current place.
- **/help** - Output help message.
- **/cancel** - Cancel action.
---
## Start telegram bot
Before start python script need open *[config.py][config.py]* and enter your telegram bot and AccuWeather tokens.

[config.py][config.py]
```python
telegram_key = "xxx" #your telegram bot token
weather_key = "xxx"  #your AccuWeather token
```
Selection format for saving users data is implemented. For selection format is need open file *[tbweather.py][tbweather.py]* and correct 6 and 34 line in this file.

- For saving users data in *[json format][users.json]* :
```python
6 | from Database import JSON
  |...
34| db = JSON(path = "users.json", indent = 4)
```
- For saving users data in *[csv format][users.csv]* :
```python
6 | from Database import CSV
  |...
34| db = CSV(path = "users.csv", delimiter = ";")
```
- For saving users data in *[yaml format][users.yaml]* :
```python
6 | from Database import YAML
  |...
34| db = YAML(path = "users.yaml", indent = 2)
```

Command for install telegram weather bot *[requirements][requirements.txt]*:
```bash
pip install -r requirements.txt
```

Command for start python script :
```bash
python tb_weather/tbweather.py
```
---
[config.py]: https://github.com/two-dimensional-array/telegram_weather_bot/blob/master/tb_weather/config.py
[tbweather.py]: https://github.com/two-dimensional-array/telegram_weather_bot/blob/master/tb_weather/tbweather.py
[users.json]: https://github.com/two-dimensional-array/telegram_weather_bot/blob/master/tb_weather/users.json
[users.csv]: https://github.com/two-dimensional-array/telegram_weather_bot/blob/master/tb_weather/users.csv
[users.yaml]: https://github.com/two-dimensional-array/telegram_weather_bot/blob/master/tb_weather/users.yaml
[requirements.txt]: https://github.com/two-dimensional-array/telegram_weather_bot/blob/master/requirements.txt
