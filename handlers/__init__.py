# Create files for handlers in this folder.
from telebot import TeleBot

from .spam_command import anti_spam
from .core_handlers import register_core_handlers
from .payments import register_payments_handlers


def register_handlers(bot: TeleBot):
    bot.register_message_handler(anti_spam, commands=['spam'], pass_bot=True)
    register_core_handlers(bot)
    register_payments_handlers(bot)