import telebot
import requests

API_KEYS = {
    "telegram": "\/",
    "probivapi": "\/"
}

bot = telebot.TeleBot(API_KEYS["telegram"])

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Привет! Я бот для поиска информации о почте и телефоне. Введите /email <email> или /phone <номер телефона> для поиска.")
    bot.send_message(message.chat.id, 'developer: @kamiderer| github: https://github.com/kamiq1337')
@bot.message_handler(commands=['email'])
def email_search(message):
    query = message.text.split(' ')[1]
    process_email_search(message, query)

@bot.message_handler(commands=['phone'])
def phone_search(message):
    query = message.text.split(' ')[1]
    process_phone_search(message, query)

def process_email_search(message, query):
    response = requests.get(f'https://probivapi.com/api/email/info/{query}', headers={'x-auth': API_KEYS["probivapi"]})
    
    if response.status_code == 200:
        data = response.json()
        formatted_data = format_data(data)
        bot.send_message(message.chat.id, f'Информация по email {query}:\n{formatted_data}')
    else:
        bot.send_message(message.chat.id, 'Ошибка при получении информации. Попробуйте еще раз.')

def process_phone_search(message, query):
    response = requests.get(f'https://probivapi.com/api/phone/info/{query}', headers={'x-auth': API_KEYS["probivapi"]})
    
    if response.status_code == 200:
        data = response.json()
        formatted_data = format_data(data)
        bot.send_message(message.chat.id, f'Информация по номеру телефона {query}:\n{formatted_data}')
    else:
        bot.send_message(message.chat.id, 'Ошибка при получении информации. Попробуйте еще раз.')

def format_data(data):
    formatted_data = ''
    for key, value in data.items():
        if isinstance(value, dict):
            formatted_data += f'\n{key}:'
            for k, v in value.items():
                formatted_data += f'\n- {k}: {v}'
        else:
            formatted_data += f'\n{key}: {value}'
    return formatted_data

bot.polling()
