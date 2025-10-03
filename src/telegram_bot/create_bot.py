import logging
from pathlib import Path

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.redis import RedisStorage
from decouple import AutoConfig

BASE_DIR = Path(__file__).resolve().parent.parent.parent

config = AutoConfig(search_path=BASE_DIR)

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

storage = RedisStorage.from_url(
    f"redis://{config("REDIS_USER")}:{config("REDIS_PASSWORD")}@{config("REDIS_HOST")}:{config("REDIS_PORT")}/0"
)

bot = Bot(
    token=config("BOT_TOKEN"), default=DefaultBotProperties(parse_mode=ParseMode.HTML)
)
dp = Dispatcher(storage=storage)
