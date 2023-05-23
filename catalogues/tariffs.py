from telebot.types import LabeledPrice, ShippingOption

# More about Payments: https://core.telegram.org/bots/payments

PRICES = [LabeledPrice(label='Working Time Machine', amount=5750), LabeledPrice('Gift wrapping', 500)]

SHIPPING_OPTIONS = [
    ShippingOption(id='instant', title='WorldWide Teleporter').add_price(LabeledPrice('Teleporter', 1000)),
    ShippingOption(id='pickup', title='Local pickup').add_price(LabeledPrice('Pickup', 300))]

class TimeMachine():
    title = "Working Time Machine"
    description = "Want to visit your great-great-great-grandparents? Make a fortune at the races? " \
                  "Shake hands with Hammurabi and take a stroll in the Hanging Gardens? " \
                  "Order our Working Time Machine today!"
    invoice_payload = "HAPPY FRIDAYS COUPON",
    currency = "rub"
    photo_url = 'http://erkelzaar.tsudao.com/models/perrotta/TIME_MACHINE.jpg',