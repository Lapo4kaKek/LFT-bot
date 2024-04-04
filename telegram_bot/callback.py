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
        # Запрос на создание новой стратегии.
        command = re.split('create_', text_data.data, maxsplit=1)[1]
        if re.match('type_', command):
            # Создание стратегии определенного типа.
            type = re.split('type_', text_data.data, maxsplit=1)[1]
            try:
                message_id = bot.edit_message_text(chat_id=chat_id,
                                                   message_id=text_data.message.message_id,
                                                   text=texts.create_strategy(),
                                                   reply_markup=keyboards.create_strategy(),
                                                   parse_mode='html').message_id
            except Exception as err:
                print(str(err))
                # admin.error('Create new text callback ' + str(err))
        else:
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
        # Вывод всех стратегий.
        try:
            message_id = bot.edit_message_text(chat_id=chat_id,
                                               message_id=text_data.message.message_id,
                                               text=texts.all_strategies(),
                                               reply_markup=keyboards.all_strategies(),
                                               parse_mode='html').message_id
        except Exception as err:
            print(str(err))
    elif re.match('entity', command):
        try:
            strategy_id = re.split('entity_', text_data.data, maxsplit=1)[1]
            message_id = bot.edit_message_text(chat_id=chat_id,
                                               message_id=text_data.message.message_id,
                                               text=texts.strategy_info(strategy_id),
                                               reply_markup=keyboards.strategy_info(strategy_id),
                                               parse_mode='html').message_id
        except Exception as err:
            print(str(err))
    elif re.match('back', command):
        # Нажатие на кнопку возврата.
        try:
            message_id = bot.edit_message_text(chat_id=chat_id,
                                               message_id=text_data.message.message_id,
                                               text=texts.strategy_actions(),
                                               reply_markup=keyboards.strategy_actions(),
                                               parse_mode='html').message_id
        except Exception as err:
            print(str(err))
