"""
Тексты для сообщений.

"""
import json
import pprint
import strategy.strategy_manager
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
    for type in strategy.strategy_manager.strategies_types:
        text += str(num) + ". " + type + '\n'
        num += 1
    text += '</code>'

    return text


def create_strategy_type(type):
    """
    Вывод сообщения для создания определённой стратегии.
    :param type Тип создаваемой стратегии.
    :return: Str.
    """
    text = '<b>To create a strategy, send the following message with modified parameters:</b>\n'
    text += '<pre>'
    text += f"#CREATE_STRATEGY\n"
    text += json.dumps(strategy.strategy_manager.strategies_types[type], indent=4)
    text += '</pre>'
    return text


def all_strategies(database):
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


def strategy_info(database, strategy_id):
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
        text = '<b>🔹 Strategy Details 🔹</b>\n\n'
        text += '<b>Title:</b> <i>' + strategy_data['name'] + '</i>\n'
        text += '<b>Type:</b> <i>' + strategy_data['type'] + '</i>\n'
        text += '<b>Exchange:</b> <i>' + strategy_data['exchange'] + '</i>\n'
        text += '<b>Symbol:</b> <i>' + strategy_data['symbol'] + '</i>\n'
        text += '<b>Balance:</b> <i>' + str(round(strategy_data['balance'], 5)) + '</i>\n'
        text += '<b>Assets Number:</b> <i>' + str(round(strategy_data['assetsNumber'], 5)) + '</i>\n'
        text += '<b>Status:</b> <i>' + ('launched' if strategy_data['status'] else 'stopped') + '</i>\n'
        text += '<b>Created:</b> <i>' + str(strategy_data['createdTime']) + '</i>\n'
        return text
    except Exception as err:
        print(err)
        # admin.error(error_admin_text='Не получилось содздать описание текста' + str(err))
        return None
