from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from keyboards.all_keyboards import main_kb

start_router = Router()

@start_router.message(Command('start'))
async def cmd_start(message: Message):
    message.from_user.first_name
    await message.answer(f'{message.from_user.first_name}:{message.from_user.last_name}',
                         reply_markup=main_kb())