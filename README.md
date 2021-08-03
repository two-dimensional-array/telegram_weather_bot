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
- Before start python script need open *[config.py][config.py]* and enter your telegram bot and AccuWeather tokens.

  [config.py][config.py]
  ```python
  telegram_key = "xxx" #your telegram bot token
  weather_key = "xxx"  #your AccuWeather token
  ```
- Selection format for saving users data is implemented. For selection format (default format is *[yaml][users.yaml]*) is need open file *[tbweather.py][tbweather.py]* and correct *[6][tbweather.py_l6]* and *[37][tbweather.py_l34]* line in this file.

  - For saving users data in *[json format][users.json]* :
  ```python
  6 | from Database import JSON
    | ...
  34| db = JSON(path = "users.json", indent = 4)
  ```
  - For saving users data in *[csv format][users.csv]* :
  ```python
  6 | from Database import CSV
    | ...
  34| db = CSV(path = "users.csv", delimiter = ";")
  ```
  - For saving users data in *[yaml format][users.yaml]* :
  ```python
  6 | from Database import YAML
    | ...
  34| db = YAML(path = "users.yaml", indent = 2)
  ```

- Startup *[telegram weather bot pyhton script][tbweather.py]* is implemented by bash script *[start.sh][start.sh]*.

  Commands for first start *[python script][tbweather.py]* :
  ```bash
  ~/repository_directory/start.sh -i
  ```
  or
  ```bash
  ~/repository_directory/start.sh --install
  ```
  This commands is install telegram weather bot *[requirements][requirements.txt]* and run *[python script][tbweather.py]*.

  - Commands for run telegram weather bot *[python script][tbweather.py]* without installing *[requirements][requirements.txt]* :
  ```bash
  ~/repository_directory/start.sh -r
  ```
  or
  ```bash
  ~/repository_directory/start.sh --run
  ```

  - Commands for output help message of bash script *[start.sh][start.sh]* :
  ```bash
  ~/repository_directory/start.sh -h
  ```
  or
  ```bash
  ~/repository_directory/start.sh --help
  ```
---
[config.py]: https://github.com/two-dimensional-array/telegram_weather_bot/blob/master/tb_weather/config.py
[tbweather.py]: https://github.com/two-dimensional-array/telegram_weather_bot/blob/master/tb_weather/tbweather.py
[tbweather.py_l6]: https://github.com/two-dimensional-array/telegram_weather_bot/blob/a1cb244f564033996bc71629d162131804723bc8/tb_weather/tbweather.py#L6
[tbweather.py_l37]: https://github.com/two-dimensional-array/telegram_weather_bot/blob/a1cb244f564033996bc71629d162131804723bc8/tb_weather/tbweather.py#L37
[users.json]: https://github.com/two-dimensional-array/telegram_weather_bot/blob/master/tb_weather/users.json
[users.csv]: https://github.com/two-dimensional-array/telegram_weather_bot/blob/master/tb_weather/users.csv
[users.yaml]: https://github.com/two-dimensional-array/telegram_weather_bot/blob/master/tb_weather/users.yaml
[requirements.txt]: https://github.com/two-dimensional-array/telegram_weather_bot/blob/master/requirements.txt
[start.sh]: https://github.com/two-dimensional-array/telegram_weather_bot/blob/master/start.sh
