import re

from main import bot
from telegram_bot import texts, keyboards


def strategy(text_data):
    """
    Обработка нажатия на кнопки, связанные со стратегиями.
    :param text_data: Информация о callback.
    """
    chat_id = str(text_data.from_user.id)
    command = re.split('strategy_', text_data.data, maxsplit=1)[1]

    if re.match('create', command):
        try:
            message_id = bot.edit_message_text(chat_id=chat_id,
                                               message_id=text_data.message.message_id,
                                               text=texts.create_strategy(),
                                               reply_markup=keyboards.create_strategy(),
                                               parse_mode='html').message_id
        except Exception as err:
            print(str(err))
            # admin.error('Create new text callback ' + str(err))
    elif re.match('all', command):
        try:
            message_id = bot.edit_message_text(chat_id=chat_id,
                                               message_id=text_data.message.message_id,
                                               text=texts.all_strategies(),
                                               reply_markup=keyboards.all_strategies(),
                                               parse_mode='html').message_id
        except Exception as err:
            print(str(err))
    elif re.match('type_', command):
        command = re.split('type_', text_data.data, maxsplit=1)[1]
        # Обработка нужного типа стратегии
    elif re.match('back', command):
        try:
            message_id = bot.edit_message_text(chat_id=chat_id,
                                               message_id=text_data.message.message_id,
                                               text=texts.strategy_actions(),
                                               reply_markup=keyboards.strategy_actions(),
                                               parse_mode='html').message_id
        except Exception as err:
            print(str(err))
