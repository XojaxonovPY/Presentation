from aiogram import Dispatcher

from bot.handlers import router as main_handler

dp = Dispatcher()

dp.include_router(main_handler)
