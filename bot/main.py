import os
import sys

from aiogram.client.session.aiohttp import AiohttpSession

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'root.settings')

import django

django.setup()
from os import getenv
import asyncio
import sys
import logging
from os.path import join
from pathlib import Path
from aiogram import Bot
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from dotenv import load_dotenv

from bot.dispatcher import dp

path = Path(__file__).parent.parent
ENV_PATH = join(path, '.env')

load_dotenv(ENV_PATH)
BOT_TOKEN = getenv('BOT_TOKEN')
session = AiohttpSession(timeout=60)


async def main() -> None:
    bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML), session=session)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
