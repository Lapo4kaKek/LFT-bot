"""
Обработчики сообщений.

"""

import os

import telebot
from dotenv import load_dotenv

from telegram_bot import keyboards, texts

load_dotenv()
telegram_bot_token = os.getenv('TELEGRAM_BOT_TOKEN')

bot = telebot.TeleBot(telegram_bot_token)

@bot.message_handler(commands=["start", "help"])
def start_chat(text_data):
    """
    :param text_data: Информация о сообщении.
    """
    if text_data.chat.type == "private":
        try:
            chat_id = str(text_data.chat.id)
            message = text_data.text
            if message == '/start':
                bot.send_message(chat_id=chat_id,
                                 text=texts.greeting(),
                                 parse_mode='html',
                                 reply_markup=keyboards.menu_static(chat_id))
        except Exception as err:
            pass
            # admin.error(error_admin_text='Первое сообщение от пользователя ' + str(err))


bot.polling(none_stop=True)