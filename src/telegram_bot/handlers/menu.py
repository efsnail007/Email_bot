import asyncio

from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.utils.chat_action import ChatActionSender

from create_bot import bot
from keyboards.all_keyboards import main_kb
from .states import Menu, AddEmail, ListEmail, DeleteEmail

menu_router = Router()


@menu_router.message(Menu.menu)
async def menu_message(message: Message, state: FSMContext):
    if "Добавить почту" in message.text:
        async with ChatActionSender.typing(bot=bot, chat_id=message.chat.id):
            await asyncio.sleep(0.2)
            await message.answer("Пожалуйста введите логин почты!")
        await state.set_state(AddEmail.login)
    elif "Список почт" in message.text:
        await state.set_state(ListEmail.list)
    elif "Удалить почту" in message.text:
        async with ChatActionSender.typing(bot=bot, chat_id=message.chat.id):
            await asyncio.sleep(0.2)
            await message.answer("Пожалуйста введите логин почты!")
        await state.set_state(DeleteEmail.delete_email)
    elif "Инструкция" in message.text:
        await message.answer("Инструкция", reply_markup=main_kb())
    else:
        await message.answer("Пожалуйста, воспользуйтесь меню", reply_markup=main_kb())
