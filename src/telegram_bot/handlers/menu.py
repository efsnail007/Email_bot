from aiogram import Router
from aiogram.types import Message

menu_router = Router()

@menu_router.message()
async def echo_message(message: Message):
    if "Добавить почту" in message.text:
        await message.answer("fsm на добавление")
    elif "Удалить почту" in message.text:
        await message.answer("fsm на удаление")
    elif "Инструкция" in message.text:
        await message.answer("Инструкция")
    else:
        await message.answer("/start")