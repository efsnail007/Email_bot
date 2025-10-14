import asyncio

from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.utils.chat_action import ChatActionSender
from create_bot import api_client, bot
from keyboards.all_keyboards import main_kb

from .states import AddEmail, Menu

add_email_router = Router()


@add_email_router.message(AddEmail.login)
async def add_login(message: Message, state: FSMContext):
    await state.update_data(login=message.text)
    async with ChatActionSender.typing(bot=bot, chat_id=message.chat.id):
        await asyncio.sleep(0.2)
        await message.answer("Супер! А теперь введите пароль:")
    await state.set_state(AddEmail.password)


@add_email_router.message(AddEmail.password)
async def add_password(message: Message, state: FSMContext):
    await state.update_data(password=message.text)
    data = await state.get_data()

    response, status = await api_client.create_email(
        message.from_user.id, data.get("login"), data.get("password")
    )
    if status == 201:
        await message.answer(
            "Почта добавлена для отслеживания!", reply_markup=main_kb()
        )
    elif status == 400:
        await message.answer("Неверный пароль!", reply_markup=main_kb())
    else:
        await message.answer("Произошла ошибка на сервере!", reply_markup=main_kb())
    await state.clear()
    await state.set_state(Menu.menu)
