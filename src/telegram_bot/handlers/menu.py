import asyncio

from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.utils.chat_action import ChatActionSender
from create_bot import api_client, bot
from keyboards.all_keyboards import main_kb
from utils.utils import get_email_list_to_text

from .states import AddEmail, DeleteEmail, Menu

menu_router = Router()


@menu_router.message(Menu.menu)
async def menu_message(message: Message, state: FSMContext):
    if "Добавить почту" in message.text:
        async with ChatActionSender.typing(bot=bot, chat_id=message.chat.id):
            await asyncio.sleep(0.2)
            await message.answer("Пожалуйста введите логин почты!")
        await state.set_state(AddEmail.login)
    elif "Список почт" in message.text:
        response, status = await api_client.get_list_email(message.from_user.id)
        if status == 200:
            await message.answer(
                get_email_list_to_text(response), reply_markup=main_kb()
            )
        else:
            await message.answer("Произошла ошибка на сервере!", reply_markup=main_kb())
    elif "Удалить почту" in message.text:
        async with ChatActionSender.typing(bot=bot, chat_id=message.chat.id):
            await asyncio.sleep(0.2)
            await message.answer("Пожалуйста введите логин почты!")
        await state.set_state(DeleteEmail.delete_email)
    elif "Инструкция" in message.text:
        await message.answer("Инструкция", reply_markup=main_kb())
    else:
        await message.answer("Пожалуйста, воспользуйтесь меню", reply_markup=main_kb())
