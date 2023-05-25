from telebot.types import ReplyKeyboardMarkup, KeyboardButton
from catalogues.button_texts import ButtonNames


def admin_markup():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    markup.add(ButtonNames.USER_STATS)
    markup.add(ButtonNames.PICK_WINNER)
    markup.add(ButtonNames.CLEAR_EVENT)

    return markup