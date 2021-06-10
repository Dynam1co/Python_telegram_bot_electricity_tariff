from dataclasses import dataclass
import conf_management as ConfMgt
from telegram.ext import Updater
from telegram.ext import CommandHandler

import scrap as scp


@dataclass
class TelegramC:
    message: str
    token: str = ConfMgt.get_telegram_token()
    chat_id: str = ConfMgt.get_telegram_group_id()

    def send_message(self):
        update = Updater(token=self.token)
        update.bot.send_message(chat_id=self.chat_id, text=self.message)

    def run_bot(self):
        updater = Updater(token=self.token)
        dispatcher = updater.dispatcher

        # Command handlers
        start_handler = CommandHandler('start', self.start)
        today_handler = CommandHandler('today', self.today)

        # Add the handlers to the bot
        dispatcher.add_handler(start_handler)
        dispatcher.add_handler(today_handler)

        # Starting the bot
        updater.start_polling()

    def start(self, bot, update):
            message = "Bienvenido, este bot informa sobre los precios de la nueva tarifa de la luz.\n\nComandos disponibles:\n  - " \
                    "today: da los precios del día"
            update.bot.send_message(chat_id=bot.message.chat_id, text=message)

    def today(self, bot, update):
        # Get data from web url
        my_day = scp.main()

        # Format message
        self.message = my_day.prepare_message()

        update.bot.send_message(chat_id=bot.message.chat_id, text=self.message)        