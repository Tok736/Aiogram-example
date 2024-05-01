import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from common.router         import router as common_router
from message_work.router   import router as message_router
from help_router           import router as help_router
from state_machine.router  import router as state_router
from buttons.router        import router as buttons_router

from config import env_config

logging.basicConfig(level=logging.INFO)

async def main():
    bot = Bot(
        token=env_config.BOT_TOKEN.get_secret_value()
    )

    dp = Dispatcher(
        storage=MemoryStorage()
    )

    dp.include_routers(
        common_router,
        message_router,
        help_router,
        state_router,
        buttons_router,
    )

    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
