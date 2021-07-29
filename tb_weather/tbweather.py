from pyowm.owm import OWM
from pyowm.utils import config
from pyowm.weatherapi25.observation import Observation
from telebot import TeleBot
from telebot.types import Message, ReplyKeyboardMarkup
from Database import YAML
from config import *

MAX_LEN_OF_PLACE = 20
BUTTON_PLACE_TEXT = "Выбрать город"
BUTTON_UPDATE_TEXT = "Обновить погоду"
BUTTON_CURRENT_PLACE_TEXT = "Текущий город"
BUTTON_HELP_TEXT = "Справка"
BUTTON_CANCEL_TEXT = "Отмена"
COMMANDS = {
    "start": ("/start"),
    "place": ("/place", BUTTON_PLACE_TEXT),
    "update": ("/update", BUTTON_UPDATE_TEXT),
    "current_place": ("/current_place", BUTTON_CURRENT_PLACE_TEXT),
    "help": ("/help", BUTTON_HELP_TEXT),
    "cancel":("/cancel", BUTTON_CANCEL_TEXT)
}
HELP_MESSAGE = "Команды:\n/place - Ввод названия города. \n/update - Обновление информации об погоде в текущем городе \n/current_place - Вывод текущего города. \n/cancel - Отмена действия. \n/help - Вывод справки по командам бота"

bot = TeleBot(telegram_key)
config_wether_manager = config.get_default_config()
config_wether_manager['language'] = 'ru'
mgr = OWM(weather_key, config=config_wether_manager).weather_manager()
control_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
control_keyboard.row(BUTTON_PLACE_TEXT, BUTTON_UPDATE_TEXT)
control_keyboard.row(BUTTON_CURRENT_PLACE_TEXT, BUTTON_HELP_TEXT)
cancel_keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
cancel_keyboard.row(BUTTON_CANCEL_TEXT)
db = YAML()

@bot.message_handler(content_types=['text'])
def main(message: Message) -> None:
    if message.text in COMMANDS["start"]:
        start_message(message.chat)
    elif message.text in COMMANDS["place"]:
        set_place(message.chat.id)
    elif message.text in COMMANDS["update"]:
        update_weather(message.chat.id)
    elif message.text in COMMANDS["current_place"]:
        current_place(message.chat.id)
    elif message.text in COMMANDS["help"]:
        help_message(message.chat.id)
    else: pass

def start_message(chat) -> None:
    db.init_user(chat.id)
    bot.send_message(chat.id, f'Здравствуйте {chat.username} !\nВас приветсвует телеграм бот созданый творцом two-dimensional-array\nДля отображения списка комманд введите /help', reply_markup=control_keyboard)

def set_place(user_id: int) -> None:
    bot.send_message(user_id, "Введите название вашего города:", reply_markup=cancel_keyboard)
    bot.register_next_step_handler_by_chat_id(user_id, request_place)

def update_weather(user_id: int) -> None:
    observation = get_current_weather(db.get_geolocation(user_id))
    if observation == None:
        bot.send_message(user_id, "Не верно введён город!\nВведите название вашего города:", reply_markup=cancel_keyboard)
        bot.register_next_step_handler_by_chat_id(user_id, request_place)
    else:
        bot.send_message(user_id, output_data(observation), reply_markup=control_keyboard)

def help_message(user_id: int) -> None:
    bot.send_message(user_id, HELP_MESSAGE, reply_markup=control_keyboard)

def current_place(user_id: int) -> None:
    bot.send_message(user_id, db.get_geolocation(user_id), reply_markup=control_keyboard)

def request_place(message: Message) -> None:
    if message.text in COMMANDS["cancel"]:
        bot.send_message(message.chat.id, "Введите команду", reply_markup=control_keyboard)
    else:
        observation = get_current_weather(message.text)
        if observation == None:
            bot.send_message(message.chat.id, "Не верно введён город!\nВведите название вашего города:", reply_markup=cancel_keyboard)
            bot.register_next_step_handler_by_chat_id(message.chat.id, request_place)
        else:
            db.set_geolocation(message.chat.id, f'{observation.location.name},{observation.location.country}')
            bot.send_message(message.chat.id, output_data(observation), reply_markup=control_keyboard)

def output_data(observation: Observation) -> str:
    weather = observation.weather
    answear  = f'В городе {observation.location.name} {weather.detailed_status}\n'
    answear += f'Температура воздуха составляет {weather.temperature("celsius")["temp"]} °C\n'
    answear += f'Влажность воздуха равняется {weather.humidity} %\n'
    answear += f'Скорость ветра состовляет {weather.wind()["speed"]} м/с\n'
    answear += f'Облачность равняется {weather.clouds} %\n'
    answear += f'Восход солнца  в {weather.sunrise_time(timeformat="date").time()} по Гринвичу\n'
    answear += f'Заход солнца в {weather.sunset_time(timeformat="date").time()} по Гринвичу\n'
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
