import os
from pathlib import Path

from telebot import TeleBot
from config import *
from utils.bot_logger import logger
from telebot.types import BotCommand

from telebot import apihelper
apihelper.ENABLE_MIDDLEWARE = True

# States storage
from telebot.storage import StateMemoryStorage

# middlewares
from middlewares import register_middleware_handlers

state_storage = StateMemoryStorage()
# I recommend increasing num_threads
bot = TeleBot(TOKEN, num_threads=5, parse_mode='markdown')

# Middlewares
register_middleware_handlers(bot)


from handlers import register_handlers
import data_base
from filters import register_filters

if __name__ == '__main__':
    logger.log(LOG_LEVEL, "Bot started")
    bot.delete_my_commands()
    bot.set_my_commands([BotCommand("start", "Принять участие в мероприятии")])
    register_filters(bot)
    register_handlers(bot)
    bot.infinity_polling(skip_pending=True)
