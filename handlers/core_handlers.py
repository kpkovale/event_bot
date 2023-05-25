from telebot import TeleBot
from telebot.types import Message, ReplyKeyboardRemove
from catalogues.message_texts import MessageTexts
from catalogues.button_texts import ButtonNames
from data_base.db_models import User, clear_users, get_user_list
from models.users_model import Admin
from keyboards.admin_keyboard import admin_markup
from telebot.apihelper import ApiTelegramException
import random
from utils.bot_logger import logger


def command_start(message: Message, bot: TeleBot):
    if not Admin.is_admin(message.from_user.id) and not User.get(telegram_id=message.from_user.id):
        new_user = User(name=message.from_user.full_name, telegram_id=message.from_user.id)
        new_user.insert()
        logger.info(f"Новый пользователь присоединился к боту: {new_user.__str__()}")
    user = User.get(telegram_id=message.from_user.id)
    if user:
        bot.send_message(message.chat.id, MessageTexts.START_MESSAGE.format(user.id))
    else:
        logger.info(f"Администратор присоединился к боту: {message.from_user.id} "
                    f"| {message.from_user.full_name}")
        bot.send_message(message.chat.id, MessageTexts.ADMIN_START_MESSAGE,
                         reply_markup=admin_markup())


def pick_winner_button_handler(message: Message, bot: TeleBot):
    # Берём список активных пользователей
    users_list = get_user_list(active=True)
    # выбираем случайного победителя
    winner = users_list[random.randrange(len(users_list))]
    # отправляем сообщение админу с информацией об участнике
    bot.send_message(message.chat.id, MessageTexts.WINNER_INFO.format(winner))
    # отправляем сообщение победителю
    if winner.name[:8] != "TestUser": # если не тестовый
        logger.info(f"Отправляю сообщение пользователю {winner.__repr__()}")
        try:
            bot.send_message(winner.telegram_id, MessageTexts.WINNER_INFO.format(winner))
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
    logger.info(f"Завершаем событие, очищаем список пользвателей")
    clear_users()
    logger.info(f"Cписок пользвателей очищен")
    bot.send_message(message.chat.id, MessageTexts.CLEAR_USERS_MESSAGE,
                     reply_markup=admin_markup())


def user_stats_button_handler(message: Message, bot: TeleBot):
    users_list = get_user_list()
    if users_list:
        logger.info(f"Вывожу список пользователей в чат админу {message.from_user.full_name}")
        bot.send_message(message.chat.id, MessageTexts.USERS_COUNT_MESSAGE.format(len(users_list)))
        text = ""
        for user in users_list:
            text += user.__str__()+"\n"
        logger.info(text)
        bot.send_message(message.chat.id, text, reply_markup=admin_markup())
    else:
        bot.send_message(message.chat.id, MessageTexts.USERS_COUNT_MESSAGE.format(0),
                         reply_markup=admin_markup())


def gen_test_users_command_handler(message: Message, bot: TeleBot):
    args = message.text.split()
    logger.info(f"Command text: {message.text}")
    if len(args) < 2:
        bot.send_message(message.chat.id, MessageTexts.GEN_USERS_USAGE, reply_markup=admin_markup())
        return
    if args[1].isdigit():
        bot.send_chat_action(message.chat.id, "typing")
        logger.info(f"Генерируем пользователей в количестве: {args[1]}")
        for i in range(1, int(args[1])+1):
            new_user = User(name=f"TestUser{i}", telegram_id=int(random.random()*1000000))
            new_user.insert()
        bot.send_message(message.chat.id, f"{args[1]} пользователей сгенерировано.",
                         reply_markup=admin_markup())


def any_text_admin_message_handler(message: Message, bot: TeleBot):
    logger.info(message.text)


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
    bot.register_message_handler(any_text_admin_message_handler, content_types=['text'],
                                 admin=True, pass_bot=True)
