# Text messages templates

class MessageTexts:
    START_MESSAGE = "Здравствуйте! Я - бот Telegram.\n" \
                    "Это сообщение выводится любому пользователю, который нажмёт команду /start"

    TERMS_MESSAGE = "Thank you for shopping with our demo bot. We hope you like your new time machine!\n" \
                    "1. If your time machine was not delivered on time, please rethink your concept " \
                    "of time and try again.\n" \
                    "2. If you find that your time machine is not working, kindly contact our future " \
                    "service workshops on Trappist-1e." \
                    " They will be accessible anywhere between May 2075 and November 4000 C.E.\n" \
                    "3. If you would like a refund, kindly apply for one yesterday and we will have " \
                    "sent it to you immediately."
    PURCHASE_MESSAGE = "Real cards won't work with me, no money will be debited from your account." \
                       " Use this test card number to pay for your Time Machine: \n<code>4242 4242 4242 4242</code>" \
                       "\n\nThis is your demo invoice:"
    PAYMENT_SUCCESS = "Hoooooray! Thanks for payment! We will proceed your order for <code>{} {}</code> " \
                      "as fast as possible! " \
                      "Stay in touch.\n\nUse /buy again to get a Time Machine for your friend!"
