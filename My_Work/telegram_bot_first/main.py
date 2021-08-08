# -*- coding: utf-8 -*-
from telegram import Bot, Update
from telegram.ext import Updater
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler
from telegram.ext import CallbackContext
from telegram.ext import Filters
from My_Work.telegram_bot_first.config import token, token_api
from telegram.utils.request import Request


def message_handler(update: Update, context: CallbackContext):
    update.message.reply_text(
        text='Привет, похоже живем!!! Ну посмотримчто в прибыли получится!!',
    )


def main():
    print('Start')

    req = Request(
        connect_timeout=0.5,
    )
    bot = Bot(
        request=req,
        token=token,  # если провайлер блочит, то переопределяем это: base_url='https://telegg.ru/orig/bot',
    )

    updater = Updater(
        bot=bot,
        use_context=True,
    )

    print(updater.bot.get_me())

    updater.dispatcher.add_handler(MessageHandler(filters=Filters.all, callback=message_handler))

    updater.start_polling()
    updater.idle()

    print('Finish')


if __name__ == '__main__':
    main()
