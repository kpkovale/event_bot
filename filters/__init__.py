# register filters here or in different folders.
from .admin_filter import AdminFilter
from .button_filter import IsButtonFilter
from telebot import TeleBot


def register_filters(bot: TeleBot):
    bot.add_custom_filter(AdminFilter())
    bot.add_custom_filter(IsButtonFilter())
