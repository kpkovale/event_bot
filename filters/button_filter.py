from telebot.custom_filters import AdvancedCustomFilter
from telebot.types import Message


class IsButtonFilter(AdvancedCustomFilter):
    key = 'is_button'

    def check(self, message: Message, values: list):
        return message.text in values
    