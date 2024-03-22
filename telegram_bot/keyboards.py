"""
Клавиатуры для сообщений.

"""

from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton

import strategy.base_strategy
from main import database


def menu_static():
    """
    Клавиатура со статичными кнопками внизу экрана.
    """
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    create_strategy_button = KeyboardButton(text="Strategy 📈")
    pnl_button = KeyboardButton(text="PnL 💲")
    keyboard.add(create_strategy_button, pnl_button)
    return keyboard


def strategy_actions():
    """
    Inline клавиатура с действиями над стратегиями.
    """
    create_strategy_button = InlineKeyboardButton(text="Create Strategy 🆕", callback_data='strategy_create')
    all_strategies_button = InlineKeyboardButton(text="All Strategies 📋", callback_data='strategy_all')
    keyboard = InlineKeyboardMarkup(row_width=1)
    keyboard.add(create_strategy_button, all_strategies_button)
    return keyboard


def numbers(callback_prefix, count):
    """
    Создание кнопок с номерами.
    :param callback_prefix: Текст для callback.
    :param count: Количество кнопок.
    :return: List, содержащий 5 столбцов с кнопками.
    """
    columns = [[], [], [], [], []]
    for i in range(count):
        button = InlineKeyboardButton(text=str(i + 1),
                                      callback_data=callback_prefix + str(i))
        columns[i % 5].append(button)

    empty_button = InlineKeyboardButton(text=' ',
                                        callback_data='None')
    while count % 5 != 0:
        columns[count % 5].append(empty_button)
        count += 1

    return columns


def create_strategy():
    """
    Inline клавиатура для выбора типа стратегии.
    """
    try:
        keyboard = InlineKeyboardMarkup(row_width=5)
        back_button = InlineKeyboardButton(text='Back to Actions ⬅️',
                                           callback_data='strategy_back')
        keyboard.add(back_button)
        columns = numbers('strategy_type_', len(strategy.base_strategy.strategies_types))

        for i in range(len(columns[0])):
            line = []
            for j in range(5):
                line.append(columns[j][i])
            keyboard.add(line[0], line[1], line[2], line[3], line[4])
        return keyboard
    except Exception as err:
        print(str(err))
        # admin.error(error_admin_text='Создание клавиатуры my_texts ' + str(err))
        return None


def all_strategies():
    """
    Inline клавиатура для выбора созданной стратегии.
    """
    try:
        keyboard = InlineKeyboardMarkup(row_width=5)
        back_button = InlineKeyboardButton(text='Back to Actions ⬅️',
                                           callback_data='strategy_back')
        keyboard.add(back_button)

        query = f"""
                    SELECT count(*)
                    FROM strategies 
                    """
        data = database.execute_query(query)
        columns = numbers('strategy_entity_', data[0][0])
        for i in range(len(columns[0])):
            line = []
            for j in range(5):
                line.append(columns[j][i])
            keyboard.add(line[0], line[1], line[2], line[3], line[4])
        return keyboard
    except Exception as err:
        print(str(err))
        # admin.error(error_admin_text='Создание клавиатуры my_texts ' + str(err))
        return None
