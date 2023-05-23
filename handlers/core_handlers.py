from telebot import TeleBot
from telebot.types import Message, ReplyKeyboardRemove
from catalogues.message_texts import MessageTexts



def command_start(message: Message, bot: TeleBot):
    bot.delete_my_commands()
    bot.send_message(message.chat.id, MessageTexts.START_MESSAGE,
                     reply_markup=ReplyKeyboardRemove(),
                     parse_mode='html')


def register_core_handlers(bot: TeleBot):
    bot.register_message_handler(command_start, commands=['start'], pass_bot=True)