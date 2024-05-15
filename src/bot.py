from aiogram import Bot

from config import env_config

bot = Bot(
    token=env_config.BOT_TOKEN.get_secret_value()
)
