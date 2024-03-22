"""
Тексты для сообщений.

"""
import strategy.base_strategy
from main import database
import texttable as table

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
    try:
        text = '<b>Select a strategy from the following:</b>\n'
        query = f"""
                SELECT 
                    name, type
                FROM strategies 
                """
        data = database.execute_query(query)
        strategies_table = table.Texttable()
        strategies_table.set_deco(table.Texttable.HEADER)
        strategies_table.set_cols_align(["l", "c", "c"])
        strategies_table.set_cols_valign(["m", "m", "m"])
        strategies_table.set_cols_dtype(['i', 't', 't'])
        strategies_table.add_row([" \n", "Name\n", "Type\n"])
        for i in range(len(data)):
            strategies_table.add_row([i + 1, data[i][0], data[i][1]])
        text += '<code>' + strategies_table.draw() + '</code>'
        return text
    except Exception as err:
        print(str(err))
        return None
