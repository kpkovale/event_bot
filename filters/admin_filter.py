from telebot.custom_filters import SimpleCustomFilter
from models.users_model import Admin


class AdminFilter(SimpleCustomFilter):
    """
    Filter for admin users
    """
    key = 'admin'

    def check(self, message):
        return Admin.is_admin(message.chat.id)