from telebot.custom_filters import SimpleCustomFilter
from telebot.types import Message
from models.users_model import Admin


class AdminFilter(SimpleCustomFilter):
    """
    Filter for admin users
    """
    key = 'admin'

    def check(self, message: Message):
        return Admin.is_admin(message.chat.id)