from aiogram import Bot
from aiogram.client.default import DefaultBotProperties
from config import BOT_TOKEN

bot = Bot(
    token=BOT_TOKEN,
    default=DefaultBotProperties(parse_mode="HTML", link_preview_is_disabled=True)
)