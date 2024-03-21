"""
Клавиатуры для сообщений.

"""

from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton


def menu_static(chat_id):
    """
    :param chat_id: Id чата.
    :return: Клавиатура со статичными кнопками внизу экрана.

    """
    try:
        keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
        create_strategy_button = KeyboardButton(text="Create Strategy 📈")
        all_strategies_button = KeyboardButton(text="All Strategies 📋")
        pnl_button = KeyboardButton(text="PnL 💲")
        keyboard.add(create_strategy_button, all_strategies_button)
        keyboard.add(pnl_button)
        return keyboard
    except Exception as err:
        # admin.error(error_admin_text='menu_static keyboard ' + str(err))
        return None
