from telebot import TeleBot
from telebot.types import Message, ReplyKeyboardRemove, CallbackQuery
from catalogues.message_texts import MessageTexts
from catalogues.button_texts import ButtonNames
from data_base.db_models import User, clear_users, get_user_list
from models.users_model import Admin
from keyboards.admin_keyboard import admin_markup
from telebot.apihelper import ApiTelegramException
import random
from utils.bot_logger import logger
from telebot.util import smart_split
from telegram_bot_pagination import InlineKeyboardPaginator


def command_start(message: Message, bot: TeleBot):
    if Admin.is_admin(message.from_user.id):
        logger.info(f"Администратор присоединился к боту: {message.from_user.id} "
                    f"| {message.from_user.full_name}")
        bot.send_message(message.chat.id, MessageTexts.ADMIN_START_MESSAGE,
                         reply_markup=admin_markup())
    elif not User.get(telegram_id=message.from_user.id):
        new_user = User(name=message.from_user.full_name, telegram_id=message.from_user.id)
        new_user.insert()
        user = User.get(telegram_id=message.from_user.id)
        logger.info(f"Новый пользователь присоединился к боту: {user.__str__()}")
        bot.send_message(message.chat.id, MessageTexts.START_MESSAGE.format(user.id))
    else:
        user = User.get(telegram_id=message.from_user.id)
        bot.send_message(message.chat.id, MessageTexts.ALREADY_ENROLLED.format(user.id))


def pick_winner_button_handler(message: Message, bot: TeleBot):
    # Берём список активных пользователей
    users_list = get_user_list(active=True)
    if not users_list:
        bot.send_message(message.chat.id, MessageTexts.NO_ACTIVE_USERS, reply_markup=admin_markup())
        return
    # выбираем случайного победителя
    winner = users_list[random.randrange(len(users_list))]
    # отправляем сообщение админу с информацией об участнике
    bot.send_message(message.chat.id, MessageTexts.WINNER_INFO.format(winner))
    # отправляем сообщение победителю
    if winner.name[:8] != "TestUser":  # если не тестовый
        logger.info(f"Отправляю сообщение пользователю {winner.__repr__()}")
        try:
            bot.send_message(winner.telegram_id, MessageTexts.WINNER_MESSAGE)
        except ApiTelegramException as e:
            if e.description == "Forbidden: bot was blocked by the user":
                logger.error(f"User {winner} has blocked the bot. Cannot send message.")
            else:
                logger.error(e)
    else:
        logger.info(f"Пользователь {winner.name} - тестовый, отправки сообщения не будет")
    # снимаем флажок активного
    winner.active = False
    winner.update()


def clear_event_button_handler(message: Message, bot: TeleBot):
    logger.info(f"Администратор {message.from_user.id} завершил событие, очищаем список пользвателей")
    clear_users()
    logger.info(f"Cписок пользвателей очищен")
    bot.send_message(message.chat.id, MessageTexts.CLEAR_USERS_MESSAGE,
                     reply_markup=admin_markup())


def user_stats_button_handler(message: Message, bot: TeleBot):
    text_list, users_count = get_users_message_list()
    if text_list:
        logger.info(f"Вывожу список пользователей в чат админу {message.from_user.full_name}")
        logger.info(f"Количество пользователей: {users_count}")
        bot.send_message(message.chat.id, MessageTexts.USERS_COUNT_MESSAGE.format(users_count))
        paginator = InlineKeyboardPaginator(page_count=len(text_list),
                                            current_page=1)
        print(paginator.markup)
        bot.send_message(message.chat.id, text_list[0], reply_markup=paginator.markup)
    else:
        bot.send_message(message.chat.id, MessageTexts.USERS_COUNT_MESSAGE.format(0),
                         reply_markup=admin_markup())


def user_paginator_callback_handler(call: CallbackQuery, bot: TeleBot):
    data = int(call.data)
    bot.answer_callback_query(call.id, text="Переключаю страницу")
    text_list, _ = get_users_message_list()
    paginator = InlineKeyboardPaginator(page_count=len(text_list),
                                        current_page=data)
    bot.edit_message_text(text_list[data-1], call.message.chat.id, call.message.id,
                          reply_markup=paginator.markup)


def get_users_message_list():
    users_list = get_user_list()
    if users_list:
        text = ""
        for user in users_list:
            text += user.__str__() + "\n\n"
        return smart_split(text, chars_per_string=740), len(users_list)
    else:
        return None, None


def gen_test_users_command_handler(message: Message, bot: TeleBot):
    args = message.text.split()
    logger.info(f"Command text: {message.text}")
    if len(args) < 2:
        bot.send_message(message.chat.id, MessageTexts.GEN_USERS_USAGE, reply_markup=admin_markup())
        return
    if args[1].isdigit():
        bot.send_chat_action(message.chat.id, "typing")
        logger.info(f"Генерируем пользователей в количестве: {args[1]}")
        for i in range(1, int(args[1]) + 1):
            new_user = User(name=f"TestUser{i}", telegram_id=int(random.random() * 1000000))
            new_user.insert()
        bot.send_message(message.chat.id, f"{args[1]} пользователей сгенерировано.",
                         reply_markup=admin_markup())


def user_content_fwd_handler(message: Message, bot: TeleBot):
    for admin in Admin.ADMINS:
        try:
            bot.forward_message(admin, message.chat.id, message.id)
        except ApiTelegramException as e:
            if e.description == "Bad Request: chat not found":
                logger.error(f"admin {admin} has not initiated chat with bot. Cannot forward message")
            else:
                logger.error(e)


def forward_content_to_users_handler(message: Message, bot: TeleBot):
    user_list = get_user_list()
    if not user_list:
        bot.send_message(message.chat.id, MessageTexts.USER_LIST_EMPTY)
        return
    if message.content_type == 'text':
        send_by_function(bot.send_message, user_list, message.text)
    elif message.content_type == 'photo':
        send_by_function(bot.send_photo, user_list, message.photo[0].file_id)
    elif message.content_type == 'document':
        send_by_function(bot.send_document, user_list, message.document.file_id)


def send_by_function(method, user_list, value):
    logger.info(value)
    for user in user_list:
        try:
            method(user.telegram_id, value)
        except ApiTelegramException as e:
            if e.description == "Forbidden: bot was blocked by the user":
                logger.error(f"User {user.telegram_id} has blocked the bot. Cannot send entity.")
            else:
                logger.error(e)


def register_core_handlers(bot: TeleBot):
    bot.register_message_handler(command_start, commands=['start'], pass_bot=True)
    bot.register_message_handler(gen_test_users_command_handler, commands=['gen_test_users'], pass_bot=True,
                                 admin=True)
    bot.register_message_handler(pick_winner_button_handler, is_button=[ButtonNames.PICK_WINNER], pass_bot=True,
                                 admin=True)
    bot.register_message_handler(clear_event_button_handler, is_button=[ButtonNames.CLEAR_EVENT], pass_bot=True,
                                 admin=True)
    bot.register_message_handler(user_stats_button_handler, is_button=[ButtonNames.USER_STATS], pass_bot=True,
                                 admin=True)
    bot.register_message_handler(forward_content_to_users_handler,
                                 content_types=['text', 'photo', 'document'],
                                 admin=True, pass_bot=True)
    bot.register_message_handler(user_content_fwd_handler, content_types=['text', 'photo', 'audio',
                                                                          'voice', 'contact', 'location',
                                                                          'video', 'document'],
                                 admin=False, pass_bot=True)
    bot.register_callback_query_handler(user_paginator_callback_handler, func=lambda call: call.data.isdigit(),
                                        pass_bot=True)

