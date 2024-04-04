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


def strategy_info(strategy_id):
    """
    Информация о созданной стратегии.
    :param strategy_id: Id стратегии.
    :return: Str.
    """
    try:
        query = f"""
                SELECT 
                    *
                FROM strategies 
                WHERE strategyId == '{strategy_id}'
                """
        data = database.execute_query(query, params={'strategy_id': strategy_id}, columns=True)
        text = ""
        if data is None:
            text = 'Sorry, something went wrong.'
            return text
        strategy_data = data[0]
        text = '<b>Title:</b> ' + strategy_data['name'] + '\n'
        text += '<b>Type:</b> ' + strategy_data['type'] + '\n'
        text += '<b>Exchange:</b> ' + strategy_data['exchange'] + '\n'
        text += '<b>Symbol:</b> ' + strategy_data['symbol'] + '\n'
        text += '<b>Balance:</b> ' + str(strategy_data['balance']) + '\n'
        text += '<b>AssetsNumber:</b> ' + str(strategy_data['assetsNumber']) + '\n'
        text += '<b>Status:</b> ' + str(strategy_data['status']) + '\n'
        text += '<b>Date:</b> ' + str(strategy_data['createdTime']) + '\n'
        return text
    except Exception as err:
        print(err)
        # admin.error(error_admin_text='Не получилось содздать описание текста' + str(err))
        return None
