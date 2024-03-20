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
        main_button = KeyboardButton(text="Main")
        pnl_button = KeyboardButton(text="PnL 💲")
        keyboard.add(main_button, pnl_button)
        return keyboard
    except Exception as err:
        # admin.error(error_admin_text='menu_static keyboard ' + str(err))
        return None
