import os
from pathlib import Path

import django
from aiogram.utils.media_group import MediaGroupBuilder

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'root.settings')
django.setup()

from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message, InlineKeyboardButton, CallbackQuery, FSInputFile

from apps.models import Sprint, Product, Feature
from bot.services import inline_button_builder

router = Router()

BASE_DIR = Path(__file__).resolve().parent.parent


@router.message(CommandStart())
async def start_command_handler(message: Message):
    buttons: list[InlineKeyboardButton] | None = []
    sprints: int = 0
    async for sprint in Sprint.objects.all():
        buttons.append(InlineKeyboardButton(text=sprint.name, callback_data=f"sprint_{sprint.id}"))
        sprints += 1
    markup = inline_button_builder(buttons, [2] * (sprints // 2))
    await message.answer(text="Sprint tanlang", reply_markup=markup)


@router.callback_query(F.data.startswith('sprint_'))
async def sprint_handler(data: CallbackQuery):
    sprint_id: int = int(data.data.split('_')[1])
    buttons: list[InlineKeyboardButton] | None = []
    products: int = 0
    async for product in Product.objects.all():
        buttons.append(InlineKeyboardButton(text=product.title, callback_data=f"product_{product.id}_{sprint_id}"))
        products += 1
    markup = inline_button_builder(buttons, [2] * (products // 2))
    await data.message.answer(text="Product tanlang", reply_markup=markup)


@router.callback_query(F.data.startswith('product_'))
async def product_handler(data: CallbackQuery):
    parts = data.data.split("_")
    product_id: int = int(parts[1])
    sprint_id: int = int(parts[2])

    async for feature in Feature.objects.filter(product_id=product_id, sprint_id=sprint_id).all():
        caption = f"Title:\n{feature.title}\nDescription:\n{feature.description}"
        album_builder = MediaGroupBuilder(caption=caption)
        async for image in feature.features_files.all():
            try:
                file_path = Path(image.image.path)
            except AttributeError:
                file_path = Path.cwd() / "media" / "photo" / "features" / str(image.image)
            if file_path.is_file() and file_path.stat().st_size > 0:
                album_builder.add_photo(media=FSInputFile(file_path))
        if album_builder.build():
            await data.message.answer_media_group(media=album_builder.build())
        else:
            await data.message.answer("Afsuski, ushbu mahsulot uchun rasmlar topilmadi.")

