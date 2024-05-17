import telebot
import requests
from bs4 import BeautifulSoup
from telebot.types import ReplyKeyboardMarkup, KeyboardButton
import time
import hashlib
import os
from dotenv import load_dotenv # для хранение переменных окружения
load_dotenv() 

TOKEN_TG_BOT = os.getenv('TOKEN_TG_BOT')
"""токен для работы с API Telegram"""
bot = telebot.TeleBot(TOKEN_TG_BOT)

ANECDOTIKA_API_PID = os.getenv('ANECDOTIKA_API_PID') 
"""имя профиля"""
ANECDOTIKA_API_TOKEN = os.getenv('ANECDOTIKA_API_TOKEN')
"""засекреченый токен для работы с сайтом"""
ANECDOTIKA_API_KEY = os.getenv('ANECDOTIKA_API_KEY')
"""засекреченый ключ для работы с сайтом"""
TOKEN_TG_BOT = os.getenv('TOKEN_TG_BOT')
"""токен для работы с API Telegram"""


query = 'pid=' + ANECDOTIKA_API_PID + '&method=getRandItem&uts=' + str(int(time.time()))  # формируем строку параметров
signature = hashlib.md5((query + ANECDOTIKA_API_KEY).encode())  # получаем цифровую подпись
url = 'http://anecdotica.ru/api?' + query + '&hash=' + signature.hexdigest()



def parse_anekdot() -> str :
    """Парсит анекдот с сайта и возвращает его"""
    response = requests.get(url=url)
    print(response.status_code)
    print(response.text)
    soup = BeautifulSoup(response.text, 'xml')
    anekdot = soup.find('item').text
    return anekdot


# Обработчик сообщений
@bot.message_handler(func=lambda message: True)
def handler_messages(message):

    if message.text == '/start':
        # Набор кнопок
        markup = ReplyKeyboardMarkup(row_width=1)
        btn1 = KeyboardButton('Пришли анекдот')
        btn2 = KeyboardButton('Хватит с меня шуточек..')
        markup.add(btn1, btn2)
        bot.send_message(chat_id=message.chat.id,
                         text='Здраствуйте, для анекдотика нажми кнопочку)',
                         reply_markup= markup)
        
    elif message.text == 'Пришли анекдот':
        text_anekdot = parse_anekdot()
        if text_anekdot:
            bot.send_message(chat_id=message.chat.id, text=text_anekdot)
        else:
            print('ошибочка, шутки нету(')
    elif message.text == 'Хватит с меня шуточек..':
        bot.send_message(chat_id=message.chat.id, text='Ладно, приходите ещё!')





bot.polling(non_stop=True, interval=5)


# <item><text>— Что такое конец света? 
# — Это массовое применение системы контроля
# безопасности ядерных реакторов под управлением Windows 95.</text><note></note></item>
        

