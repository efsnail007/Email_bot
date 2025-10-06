import asyncio

from create_bot import bot, dp
from handlers.add_email import add_email_router
from handlers.menu import menu_router
from handlers.start import start_router


async def main():
    dp.include_router(start_router)
    dp.include_router(menu_router)
    dp.include_router(add_email_router)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
