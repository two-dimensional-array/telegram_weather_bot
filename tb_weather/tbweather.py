import telebot
import pyowm
import Database
from config import *

bot = telebot.TeleBot(telegram_key)
owm = pyowm.OWM(weather_key)
mgr = owm.weather_manager()
help_msg = "Команды:\n/place - Ввод названия города. \n/update - Обновление информации об погоде в текущем городе \n/current_place - Вывод текущего города. \n/help - Вывод справки по командам бота"

keyboard = telebot.types.ReplyKeyboardMarkup(True, True)
keyboard.row('/place', '/update','/current_place','/help')

db = Database.YAML()

@bot.message_handler(commands=['start'])
def start_message(message):
    db.init_user(message.chat.id)
    bot.send_message(message.chat.id, "Здравствуйте " + str(message.chat.username) + " !\nВас приветсвует телеграм бот созданый творцом two-dimensional-array\nДля отображения списка комманд введите /help",reply_markup=keyboard)

@bot.message_handler(commands=['place'])
def get_message(message):
    bot.send_message(message.chat.id, "Введите название вашего города:")
    bot.register_next_step_handler(message, ask_place)

@bot.message_handler(commands=['update'])
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

@bot.message_handler(commands=['help'])
def help_message(message):
    bot.send_message(message.chat.id, help_msg,reply_markup=keyboard)

@bot.message_handler(commands=['current_place'])
def current_place(message):
    bot.send_message(message.chat.id, db.get_geolocation(message.chat.id), reply_markup=keyboard)

def output_data(observation):
    w = observation.weather
    answear = "В городе " + observation.location.name + " " + str(w.detailed_status) + "\n"
    answear += "Температура воздуха составляет " + str(w.temperature('celsius')["temp"]) + " °C\n"
    answear += "Влажность воздуха равняется " + str(w.humidity) + "%\n"
    answear += "Скорость ветра состовляет " + str(w.wind()["speed"]) + " м/с\n"
    answear += "Облачность равняется " + str(w.clouds) + "% \n"
    answear += "Восход солнца: " + str(w.sunrise_time(timeformat='iso')) + "\n"
    answear += "Заход солнца: " + str(w.sunset_time(timeformat='iso')) + "\n"
    return answear

def get_current_weather(place):
    if place == None or len(place) > 20:
        return None
    try:
        observation = mgr.weather_at_place(place)
    except:
        return None
    else:
        return observation

bot.polling(none_stop=True)
