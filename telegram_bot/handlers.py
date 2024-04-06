"""
Обработчики сообщений.

"""

import re
from main import bot
from telegram_bot import keyboards, texts, callback

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
                                 reply_markup=keyboards.menu_static())
        except Exception as err:
            pass
            # admin.error(error_admin_text='Первое сообщение от пользователя ' + str(err))


@bot.message_handler(content_types=["text"])
def continue_chat(text_data):
    """
    :param text_data: Информация о сообщении.
    """
    try:
        if text_data.chat.type == "private":
            chat_id = str(text_data.from_user.id)
            message = text_data.text
            if message == 'Strategy 📈':
                bot.send_message(chat_id=chat_id,
                                 text=texts.strategy_actions(),
                                 reply_markup=keyboards.strategy_actions(),
                                 parse_mode='html')
            elif message == 'PnL 💲':
                pass
            elif re.match('#CREATE_STRATEGY', message):
                callback.create_new_strategy(text_data)
    except Exception as err:
        print(str(err))
        # admin.error(error_admin_text='Обработка сообщения от пользователя ' + str(err))

@bot.callback_query_handler(func=lambda text_data: True)
def callback_text(text_data):
    """
    :param text_data: Информация о сообщении.
    """

    try:
        chat_id = str(text_data.from_user.id)
        message = text_data.data
        if re.match('strategy', message):
            callback.strategy(text_data)

    except Exception as err:
        print("Callback_text " + str(err))
        # admin.error(error_admin_text='Обработка callback от пользователя ' + str(err))


bot.polling(none_stop=True)