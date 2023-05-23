from telebot import TeleBot
from telebot.types import Message, ShippingQuery, PreCheckoutQuery
from catalogues.message_texts import MessageTexts
from catalogues.tariffs import TimeMachine, PRICES, SHIPPING_OPTIONS
from catalogues.error_messages import ErrorMessages
from config import PROVIDER_TOKEN


def command_terms(message: Message, bot: TeleBot):
    bot.send_message(message.chat.id,
                     MessageTexts.TERMS_MESSAGE)


def command_buy(message: Message, bot: TeleBot):
    bot.send_message(message.chat.id, MessageTexts.PURCHASE_MESSAGE)
    bot.send_invoice(message.chat.id,  # chat_id
                     TimeMachine.title,  # title
                     TimeMachine.description,  # description
                     TimeMachine.invoice_payload,  # invoice_payload
                     PROVIDER_TOKEN,  # provider_token
                     TimeMachine.currency,  # currency
                     PRICES,  # prices
                     photo_url=TimeMachine.photo_url,
                     photo_height=512,  # !=0/None or picture won't be shown
                     photo_width=512,
                     photo_size=512,
                     is_flexible=False,  # True If you need to set up Shipping Fee
                     start_parameter='time-machine-example')


def shipping_handler(shipping_query: ShippingQuery, bot: TeleBot):
    print(shipping_query)
    bot.answer_shipping_query(shipping_query.id, ok=True,
                              shipping_options=SHIPPING_OPTIONS,
                              error_message=ErrorMessages.SHIPPING_ERROR)


def checkout_handler(pre_checkout_query: PreCheckoutQuery, bot: TeleBot):
    bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True,
                                  error_message=ErrorMessages.PRE_CHECKOUT_ERROR)


def payment_received(message: Message, bot: TeleBot):
    bot.send_message(message.chat.id,
                     MessageTexts.PAYMENT_SUCCESS.format(
                         message.successful_payment.total_amount / 100, message.successful_payment.currency))


def register_payments_handlers(bot: TeleBot):
    bot.register_message_handler(command_terms, commands=['terms'], pass_bot=True)
    bot.register_message_handler(command_buy, commands=['buy'], pass_bot=True)
    bot.register_shipping_query_handler(shipping_handler, func=lambda query: True, pass_bot=True)
    bot.register_pre_checkout_query_handler(checkout_handler, func=lambda query: True, pass_bot=True)
    bot.register_message_handler(payment_received, content_types=['successful_payment'], pass_bot=True)
