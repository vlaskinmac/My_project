# -*- coding: utf-8 -*-
import telebot

from time import sleep
import random
from telebot import types
from My_Work.telegram_bot_first.config import token

bot = telebot.TeleBot(token)


@bot.message_handler(content_types=['text'])
def text(message):
    bot.send_message(message.chat.id, 'Привет,  Максим')


if __name__ == '__main__':
    bot.polling(none_stop=True)
print(dir(telebot))
