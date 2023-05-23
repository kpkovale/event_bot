# register filters here or in different folders.
from .admin_filter import AdminFilter
from telebot import TeleBot


def register_filters(bot: TeleBot):
    bot.add_custom_filter(AdminFilter())
