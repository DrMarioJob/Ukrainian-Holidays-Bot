import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton
from datetime import datetime, timedelta

# Повний список українських свят (державні, церковні, традиційні та дні міст)
HOLIDAYS = [
    {"date": "01.01", "name": "Новий рік"},
    {"date": "07.01", "name": "Різдво Христове (за юліанським календарем)"},
    {"date": "14.01", "name": "Старий Новий рік"},
    {"date": "19.01", "name": "Водохреща"},
    {"date": "22.01", "name": "День Соборності України"},
    {"date": "15.02", "name": "Стрітення Господнє"},
    {"date": "14.02", "name": "День Святого Валентина"},
    {"date": "08.03", "name": "Міжнародний жіночий день"},
    {"date": "01.04", "name": "День сміху"},
    {"date": "07.04", "name": "Благовіщення Пресвятої Богородиці"},
    {"date": "01.05", "name": "День праці"},
    {"date": "09.05", "name": "День перемоги над нацизмом у Другій світовій війні"},
    {"date": "19.06", "name": "Трійця"},
    {"date": "28.06", "name": "День Конституції України"},
    {"date": "07.07", "name": "Івана Купала"},
    {"date": "12.07", "name": "День святих апостолів Петра і Павла"},
    {"date": "28.08", "name": "Успіння Пресвятої Богородиці"},
    {"date": "01.09", "name": "День знань"},
    {"date": "14.10", "name": "День захисників і захисниць України"},
    {"date": "21.11", "name": "День Гідності та Свободи"},
    {"date": "06.12", "name": "День Збройних сил України"},
    {"date": "13.12", "name": "День Андрія"},
    {"date": "19.12", "name": "День Святого Миколая"},
    {"date": "25.12", "name": "Різдво Христове (за григоріанським календарем)"},
    {"date": "06.01", "name": "Святвечір (за юліанським календарем)"},
    {"date": "13.01", "name": "Маланка (Щедрий вечір)"},
    {"date": "02.05", "name": "День міжнародної солідарності трудящих"},
    {"date": "24.06", "name": "Різдво Іоанна Хрестителя"},
    {"date": "01.08", "name": "Маковій (Перший Спас)"},
    {"date": "19.08", "name": "Преображення Господнє (Яблучний Спас)"},
    {"date": "29.08", "name": "Горіховий Спас"},
    {"date": "11.09", "name": "Усікновення глави Іоанна Хрестителя"},
    {"date": "14.09", "name": "Новоліття (Церковний новий рік)"},
    {"date": "27.09", "name": "Воздвиження Хреста Господнього"},
    {"date": "04.12", "name": "Введення в храм Пресвятої Богородиці"},
    {"date": "Третя субота травня", "name": "День Києва"},
    {"date": "Перша неділя вересня", "name": "День Дніпра"},
    {"date": "Перша неділя вересня", "name": "День Харкова"},
    {"date": "Друга субота вересня", "name": "День Одеси"},
    {"date": "Перша неділя жовтня", "name": "День Львова"},
    {"date": "Перша неділя вересня", "name": "День Чернігова"},
    {"date": "Перша субота жовтня", "name": "День Вінниці"}
]

# Ініціалізація бота
API_TOKEN = ''
bot = telebot.TeleBot(API_TOKEN)

# Головне меню
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    button_list = [
        KeyboardButton("Усі свята"),
        KeyboardButton("Знайти свято"),
        KeyboardButton("Найближче свято"),
        KeyboardButton("⬅ Назад")
    ]
    markup.add(*button_list)
    bot.send_message(
        message.chat.id,
        "Привіт! Я бот для перегляду українських свят. Обери дію з меню:",
        reply_markup=markup
    )

# Виведення списку всіх свят
@bot.message_handler(func=lambda message: message.text == "Усі свята")
def show_all_holidays(message):
    response = "Українські свята:\n"
    for holiday in HOLIDAYS:
        response += f"{holiday['date']} - {holiday['name']}\n"
    bot.send_message(message.chat.id, response)

# Пошук свята за ключовим словом
@bot.message_handler(func=lambda message: message.text == "Знайти свято")
def ask_for_keyword(message):
    msg = bot.send_message(message.chat.id, "Введіть ключове слово для пошуку:")
    bot.register_next_step_handler(msg, find_holiday)

def find_holiday(message):
    keyword = message.text.lower()
    found_holidays = [
        holiday for holiday in HOLIDAYS
        if keyword in holiday['name'].lower()
    ]
    if found_holidays:
        response = "Знайдені свята:\n"
        for holiday in found_holidays:
            response += f"{holiday['date']} - {holiday['name']}\n"
    else:
        response = "Свята не знайдено. Спробуйте інше ключове слово."
    bot.send_message(message.chat.id, response)

# Знаходження найближчого свята
@bot.message_handler(func=lambda message: message.text == "Найближче свято")
def next_holiday(message):
    today = datetime.now()
    upcoming_holidays = []

    for holiday in HOLIDAYS:
        try:
            holiday_date = datetime.strptime(f"{today.year}.{holiday['date']}", "%Y.%d.%m")
            if holiday_date >= today:
                upcoming_holidays.append((holiday_date, holiday['name']))
        except ValueError:
            continue  # Пропустити нерухомі свята

    if upcoming_holidays:
        upcoming_holidays.sort()
        next_holiday_date, next_holiday_name = upcoming_holidays[0]
        days_left = (next_holiday_date - today).days
        response = f"Найближче свято: {next_holiday_name} ({next_holiday_date.strftime('%d.%m.%Y')}).\nЗалишилось {days_left} днів."
    else:
        response = "Свят більше не знайдено цього року."

    bot.send_message(message.chat.id, response)

# Обробник будь-якого іншого тексту
@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.send_message(message.chat.id, "Будь ласка, оберіть дію з меню або скористайтесь пошуком.")

# Запуск бота
if __name__ == '__main__':
    bot.polling(none_stop=True)
