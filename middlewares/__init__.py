# Create files for your middlewares in this folder.
from telebot import TeleBot
from .antiflood_middleware import antispam_func


def register_middleware_handlers(bot: TeleBot):
    # Middlewares
    bot.register_middleware_handler(antispam_func, update_types=['message'])