# Create your states in this folder.
from telebot.handler_backends import State, StatesGroup


class MyStates(StatesGroup):
    """
    Group of states for registering
    """
    state1 = State()
    state1.name = 'state1'
    state2 = State()
    state2.name = 'state2'
