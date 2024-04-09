"""
Обработчики сообщений.

"""
import re

import telebot
from telegram_bot import keyboards, texts, callback
from telegram_bot.callback import TelegramBotCallback


class TelegramBotHandlers:
    def __init__(self, monitoring, database, telegram_bot_token):
        self.monitoring = monitoring
        self.database = database
        self.bot = telebot.TeleBot(telegram_bot_token)
        self.callback = TelegramBotCallback(self.monitoring, self.database, self.bot)

        @self.bot.message_handler(commands=["start", "help"])
        def start_chat(text_data):
            """
            :param text_data: Информация о сообщении.
            """
            if text_data.chat.type == "private":
                try:
                    chat_id = str(text_data.chat.id)
                    message = text_data.text
                    if message == '/start':
                        self.bot.send_message(chat_id=chat_id,
                                              text=texts.greeting(),
                                              parse_mode='html',
                                              reply_markup=keyboards.menu_static())
                except Exception as err:
                    pass
                    # admin.error(error_admin_text='Первое сообщение от пользователя ' + str(err))

        @self.bot.message_handler(content_types=["text"])
        def continue_chat(text_data):
            print(text_data)
            """
            :param text_data: Информация о сообщении.
            """
            try:
                if text_data.chat.type == "private":
                    chat_id = str(text_data.from_user.id)
                    message = text_data.text
                    if message == 'Strategy 📈':
                        self.bot.send_message(chat_id=chat_id,
                                              text=texts.strategy_actions(),
                                              reply_markup=keyboards.strategy_actions(),
                                              parse_mode='html')
                    elif message == 'PnL 💲':
                        self.bot.send_message(chat_id=chat_id,
                                              text=texts.pnl(database, monitoring),
                                              parse_mode='html')
                    elif re.match('#CREATE_STRATEGY', message):
                        self.callback.create_new_strategy(text_data)
            except Exception as err:
                print(str(err))
                # admin.error(error_admin_text='Обработка сообщения от пользователя ' + str(err))

        @self.bot.callback_query_handler(func=lambda text_data: True)
        def callback_text(text_data):
            print(text_data)
            """
            :param text_data: Информация о сообщении.
            """

            try:
                chat_id = str(text_data.from_user.id)
                message = text_data.data
                if re.match('strategy', message):
                    self.callback.strategy(text_data)

            except Exception as err:
                print("Callback_text " + str(err))
                # admin.error(error_admin_text='Обработка callback от пользователя ' + str(err))

    def start_bot(self):
        self.bot.polling(none_stop=True)
