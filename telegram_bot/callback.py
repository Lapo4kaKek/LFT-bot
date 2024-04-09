import asyncio
import json
import re

import strategy.strategy_manager
from strategy.strategy_manager import register_strategy
from telegram_bot import texts, keyboards


class TelegramBotCallback:
    def __init__(self, monitoring, database, bot):
        self.monitoring = monitoring
        self.database = database
        self.bot = bot

    def create_new_strategy(self, text_data):
        """
        Создание новой стратегии по заданному JSON.
        :param text_data: json для создания стратегии.
        """
        chat_id = str(text_data.from_user.id)
        command = re.split('#CREATE_STRATEGY', text_data.text, maxsplit=1)[1]
        data = json.loads(command)
        strategy_id = register_strategy(monitoring=self.monitoring, name=data['strategy_name'], strategy_type=data['type'],
                                        exchange=data['exchange'], symbol=data['symbol'], balance=data['balance'],
                                        settings=data['settings'])
        self.bot.delete_message(chat_id=chat_id, message_id=text_data.message_id)
        message_id = self.bot.send_message(chat_id=chat_id,
                                           text=texts.strategy_info(self.database, self.monitoring, strategy_id),
                                           reply_markup=keyboards.strategy_info(strategy_id),
                                           parse_mode='html').message_id

    def strategy(self, text_data):
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
                        message_id = self.bot.edit_message_text(chat_id=chat_id,
                                                                message_id=text_data.message.message_id,
                                                                text=texts.create_strategy(),
                                                                reply_markup=keyboards.create_strategy(),
                                                                parse_mode='html').message_id
                    else:
                        message_id = self.bot.edit_message_text(chat_id=chat_id,
                                                                message_id=text_data.message.message_id,
                                                                text=texts.create_strategy_type(command),
                                                                reply_markup=keyboards.create_strategy_type(),
                                                                parse_mode='html').message_id
                except Exception as err:
                    print(str(err))
                    # admin.error('Create new text callback ' + str(err))
            elif re.match('menu', command):
                try:
                    message_id = self.bot.edit_message_text(chat_id=chat_id,
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
                message_id = self.bot.edit_message_text(chat_id=chat_id,
                                                        message_id=text_data.message.message_id,
                                                        text=texts.all_strategies(self.database),
                                                        reply_markup=keyboards.all_strategies(self.database),
                                                        parse_mode='html').message_id
            except Exception as err:
                print(str(err))
        elif re.match('entity', command):
            try:
                strategy_id = re.split('entity_', text_data.data, maxsplit=1)[1]
                message_id = self.bot.edit_message_text(chat_id=chat_id,
                                                        message_id=text_data.message.message_id,
                                                        text=texts.strategy_info(self.database, self.monitoring, strategy_id),
                                                        reply_markup=keyboards.strategy_info(strategy_id),
                                                        parse_mode='html').message_id
            except Exception as err:
                print(str(err))
        elif re.match('back', command):
            # Нажатие на кнопку возврата.
            try:
                message_id = self.bot.edit_message_text(chat_id=chat_id,
                                                        message_id=text_data.message.message_id,
                                                        text=texts.strategy_actions(),
                                                        reply_markup=keyboards.strategy_actions(),
                                                        parse_mode='html').message_id
            except Exception as err:
                print(str(err))
        elif re.match('start', command):
            # Нажатие на кнопку запуска.
            try:
                strategy_id = re.split('start_', text_data.data, maxsplit=1)[1]
                strategy.strategy_manager.start_strategy(strategy_id)
                message_id = self.bot.edit_message_text(chat_id=chat_id,
                                                        message_id=text_data.message.message_id,
                                                        text=texts.strategy_info(self.database, self.monitoring, strategy_id),
                                                        reply_markup=keyboards.strategy_info(strategy_id),
                                                        parse_mode='html').message_id
            except Exception as err:
                print(str(err))
        elif re.match('stop', command):
            # Нажатие на кнопку остановки.
            try:
                strategy_id = re.split('stop_', text_data.data, maxsplit=1)[1]
                strategy.strategy_manager.stop_strategy(strategy_id, self.monitoring)
                message_id = self.bot.edit_message_text(chat_id=chat_id,
                                                        message_id=text_data.message.message_id,
                                                        text=texts.strategy_info(self.database, self.monitoring, strategy_id),
                                                        reply_markup=keyboards.strategy_info(strategy_id),
                                                        parse_mode='html').message_id
            except Exception as err:
                print(str(err))
        elif re.match('delete', command):
            # Нажатие на кнопку удаления стратегии.
            try:
                if re.match('delete_yes', command):
                    strategy_id = re.split('delete_yes_', text_data.data, maxsplit=1)[1]
                    strategy.strategy_manager.stop_strategy(strategy_id, self.monitoring)
                    self.monitoring.delete_strategy(strategy_id)
                    message_id = self.bot.edit_message_text(chat_id=chat_id,
                                                            message_id=text_data.message.message_id,
                                                            text=texts.all_strategies(self.database),
                                                            reply_markup=keyboards.all_strategies(self.database),
                                                            parse_mode='html').message_id
                else:
                    strategy_id = re.split('delete_', text_data.data, maxsplit=1)[1]
                    message_id = self.bot.edit_message_text(chat_id=chat_id,
                                                            message_id=text_data.message.message_id,
                                                            text=texts.delete_strategy(),
                                                            reply_markup=keyboards.delete_strategy(strategy_id),
                                                            parse_mode='html').message_id
            except Exception as err:
                print(str(err))