from aiogram.fsm.state import State, StatesGroup


class AddEmail(StatesGroup):
    login = State()
    password = State()


class ListEmail(StatesGroup):
    list = State()


class DeleteEmail(StatesGroup):
    delete_email = State()


class Menu(StatesGroup):
    menu = State()
