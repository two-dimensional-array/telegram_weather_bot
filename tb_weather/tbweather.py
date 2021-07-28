from pyowm.owm import OWM
from pyowm.weatherapi25.observation import Observation
from telebot import TeleBot
from telebot.types import ReplyKeyboardMarkup
from Database import YAML
from config import *

MAX_LEN_OF_PLACE = 20
COMMANDS = {
    "start": ("/start"),
    "place": ("/place","place"),
    "update": ("/update","update"),
    "current_place": ("/current_place","current_place"),
    "help": ("/help","help")
}

bot = TeleBot(telegram_key)
mgr = OWM(weather_key).weather_manager()
help_msg = "Команды:\n/place - Ввод названия города. \n/update - Обновление информации об погоде в текущем городе \n/current_place - Вывод текущего города. \n/help - Вывод справки по командам бота"

keyboard = ReplyKeyboardMarkup(True, True)
keyboard.row('/place', '/update','/current_place','/help')

db = YAML()

@bot.message_handler(content_types=['text'])
def main(message):
    if message.text in COMMANDS["start"]:
        start_message(message)
    elif message.text in COMMANDS["place"]:
        get_place(message)
    elif message.text in COMMANDS["update"]:
        update(message)
    elif message.text in COMMANDS["current_place"]:
        current_place(message)
    elif message.text in COMMANDS["help"]:
        help_message(message)
    else: pass

def start_message(message):
    db.init_user(message.chat.id)
    bot.send_message(message.chat.id, "Здравствуйте " + str(message.chat.username) + " !\nВас приветсвует телеграм бот созданый творцом two-dimensional-array\nДля отображения списка комманд введите /help",reply_markup=keyboard)

def get_place(message):
    bot.send_message(message.chat.id, "Введите название вашего города:")
    bot.register_next_step_handler(message, ask_place)

def update(message):
    observation = get_current_weather(db.get_geolocation(message.chat.id))
    if observation == None:
        bot.send_message(message.chat.id, "Не верно введён город!\nВведите название вашего города:")
        bot.register_next_step_handler_by_chat_id(message.chat.id, ask_place)
    else:
        bot.send_message(message.chat.id, output_data(observation),reply_markup=keyboard)

def ask_place(message):
    observation = get_current_weather(message.text)
    if observation == None:
        bot.send_message(message.chat.id, "Не верно введён город!\nВведите название вашего города:")
        bot.register_next_step_handler_by_chat_id(message.chat.id, ask_place)
    else:
        db.set_geolocation(message.chat.id, f'{observation.location.name},{observation.location.country}')
        bot.send_message(message.chat.id, output_data(observation),reply_markup=keyboard)

def help_message(message):
    bot.send_message(message.chat.id, help_msg,reply_markup=keyboard)

def current_place(message):
    bot.send_message(message.chat.id, db.get_geolocation(message.chat.id), reply_markup=keyboard)

def output_data(observation: Observation) -> str:
    w = observation.weather
    answear = f'В городе {observation.location.name} {w.detailed_status}\n'
    answear += f'Температура воздуха составляет {w.temperature("celsius")["temp"]} °C\n'
    answear += f'Влажность воздуха равняется {w.humidity} %\n'
    answear += f'Скорость ветра состовляет {w.wind()["speed"]} м/с\n'
    answear += f'Облачность равняется {w.clouds} %\n'
    answear += f'Восход солнца: {w.sunrise_time(timeformat="iso")}\n'
    answear += f'Заход солнца: {w.sunset_time(timeformat="iso")}\n'
    return answear

def get_current_weather(place: str) -> Observation or None:
    if place == None or len(place) > MAX_LEN_OF_PLACE:
        return None
    try:
        observation = mgr.weather_at_place(place)
    except:
        return None
    else:
        return observation

bot.polling(none_stop=True)
