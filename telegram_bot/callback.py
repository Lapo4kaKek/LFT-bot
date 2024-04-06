import json
import re

from main import bot
from strategy.manager import register_strategy
from telegram_bot import texts, keyboards
from main import monitoring


def create_new_strategy(text_data):
    """
    Создание новой стратегии по заданному JSON.
    :param text_data: json для создания стратегии.
    """
    chat_id = str(text_data.from_user.id)
    command = re.split('#CREATE_STRATEGY', text_data.text, maxsplit=1)[1]
    data = json.loads(command)
    register_strategy(monitoring=monitoring, name=data['strategy_name'], strategy_type=data['type'],
                                       exchange=data['exchange'], symbol=data['symbol'], balance=data['balance'],
                                       settings=data['settings'])


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
            command = re.split('type_', text_data.data, maxsplit=1)[1]
            try:
                if re.match('back', command):
                    message_id = bot.edit_message_text(chat_id=chat_id,
                                                       message_id=text_data.message.message_id,
                                                       text=texts.create_strategy(),
                                                       reply_markup=keyboards.create_strategy(),
                                                       parse_mode='html').message_id
                else:
                    message_id = bot.edit_message_text(chat_id=chat_id,
                                                       message_id=text_data.message.message_id,
                                                       text=texts.create_strategy_type(command),
                                                       reply_markup=keyboards.create_strategy_type(),
                                                       parse_mode='html').message_id
            except Exception as err:
                print(str(err))
                # admin.error('Create new text callback ' + str(err))
        elif re.match('menu', command):
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
