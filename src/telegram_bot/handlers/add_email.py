import asyncio
from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.utils.chat_action import ChatActionSender

from create_bot import bot
from keyboards.all_keyboards import main_kb
from .states import Menu, AddEmail

add_email_router = Router()


@add_email_router.message(AddEmail.login)
async def add_login(message: Message, state: FSMContext):
    await state.update_data(email=message.text)
    async with ChatActionSender.typing(bot=bot, chat_id=message.chat.id):
        await asyncio.sleep(0.2)
        await message.answer("Супер! А теперь напиши сколько тебе полных лет:")
    await state.set_state(AddEmail.password)


@add_email_router.message(AddEmail.password)
async def add_password(message: Message, state: FSMContext):
    await state.update_data(password=message.text)
    data = await state.get_data()
    msg_text = f'{data.get("email")} и {data.get("password")}'
    await message.answer(msg_text, reply_markup=main_kb())
    await state.clear()
    await state.set_state(Menu.menu)
