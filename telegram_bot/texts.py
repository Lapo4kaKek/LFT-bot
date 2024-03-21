"""
Тексты для сообщений.

"""
import strategy.base_strategy


def greeting():
    """
    Текст-приветствие.
    :return: Str.
    """
    text = 'Welcome to the <b>CryptoTrading</b> bot!'
    return text


def strategy_actions():
    """
    Действия со стратегиями.
    :return: Str.
    """
    text = '<b>Choose an action:</b>\n'
    return text


def create_strategy():
    """
    Создание стратегии.
    :return: Str.
    """
    text = '<b>Select a strategy type from the following:</b>\n'
    num = 1
    text += '<code>'
    for type in strategy.base_strategy.strategies_types:
        text += str(num) + ". " + type + '\n'
        num += 1
    text += '</code>'
    return text


def all_strategies():
    """
    Вывод всех созданных стратегий.
    :return: Str.
    """
    text = '<b>Select a strategy from the following:</b>\n'
    return text
