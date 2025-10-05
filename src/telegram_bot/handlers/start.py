from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from keyboards.all_keyboards import main_kb
from create_bot import api_client
from httpx import ConnectError
from .menu import Menu

start_router = Router()


@start_router.message(Command("start"))
async def cmd_start(message: Message, state: FSMContext):
    try:
        response, status = await api_client.get_user(tg_id=message.from_user.id)
    except ConnectError:
        await message.answer("Сервер не доступен!")
    else:
        if status == 200:
            await message.answer(
                f"Информация для старого пользователя",
                reply_markup=main_kb(),
            )
            await state.set_state(Menu.menu)
        elif status == 404:
            await api_client.create_user(
                tg_id=message.from_user.id,
                first_name=message.from_user.first_name,
                last_name=message.from_user.last_name,
            )
            await message.answer(
                f"Информация для нового пользователя",
                reply_markup=main_kb(),
            )
            await state.set_state(Menu.menu)
        elif status == 400:
            await message.answer("Произошла ошибка в телеграм!")
        else:
            await message.answer("Произошла ошибка на сервере!")
