import telebot
import pyowm
import Database

telegram_key = "xxx"
weather_key = "xxx"

bot = telebot.TeleBot(telegram_key)
owm = pyowm.OWM(weather_key)
mgr = owm.weather_manager()
help_msg = "Команды:\n/place - Ввод названия города. \n/update - Обновление информации об погоде в текущем городе \n/current_place - Вывод текущего города. \n/help - Вывод справки по командам бота"

keyboard = telebot.types.ReplyKeyboardMarkup(True, True)
keyboard.row('/place', '/update','/current_place','/help')

db = Database.JSON()

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
    place = db.get_geolocation(message.chat.id)
    if place == None or len(place) > 20:
        place = "Город не найден"
    try:
        mgr.weather_at_place(place)
    except pyowm.commons.exceptions.APIRequestError:
        bot.send_message(message.chat.id, "Не верно введён город!\nВведите название вашего города:")
        bot.register_next_step_handler_by_chat_id(message.chat.id, ask_place)
        return
    except pyowm.commons.exceptions.NotFoundError:
        bot.send_message(message.chat.id, "Не верно введён город!\nВведите название вашего города:")
        bot.register_next_step_handler_by_chat_id(message.chat.id, ask_place)
        return
    bot.send_message(message.chat.id, output_data(place), reply_markup=keyboard)

def ask_place(message):
    place = message.text
    if place == None or len(place) > 20:
        place = "Город не найден"
    try:
        mgr.weather_at_place(place)
    except pyowm.commons.exceptions.APIRequestError:
        bot.send_message(message.chat.id, "Не верно введён город!\nВведите название вашего города:")
        bot.register_next_step_handler_by_chat_id(message.chat.id, ask_place)
        return
    except pyowm.commons.exceptions.NotFoundError:
        bot.send_message(message.chat.id, "Не верно введён город!\nВведите название вашего города:")
        bot.register_next_step_handler_by_chat_id(message.chat.id, ask_place)
        return
    db.set_geolocation(message.chat.id, place)
    bot.send_message(message.chat.id, output_data(place),reply_markup=keyboard)

@bot.message_handler(commands=['help'])
def help_message(message):
    bot.send_message(message.chat.id, help_msg,reply_markup=keyboard)

@bot.message_handler(commands=['current_place'])
def current_place(message):
    bot.send_message(message.chat.id, db.get_geolocation(message.chat.id), reply_markup=keyboard)

def output_data(place):
    observation = mgr.weather_at_place(place)
    w = observation.weather
    answear = "В городе " + place + " " + str(w.detailed_status) + "\n"
    answear += "Температура воздуха составляет " + str(w.temperature('celsius')["temp"]) + " °C\n"
    answear += "Влажность воздуха равняется " + str(w.humidity) + "%\n"
    answear += "Скорость ветра состовляет " + str(w.wind()["speed"]) + " м/с\n"
    answear += "Облачность равняется " + str(w.clouds) + "% \n"
    answear += "Восход солнца: " + str(w.sunrise_time(timeformat='iso')) + "\n"
    answear += "Заход солнца: " + str(w.sunset_time(timeformat='iso')) + "\n"
    return answear

bot.polling(none_stop=True)
