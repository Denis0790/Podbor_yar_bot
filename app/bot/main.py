import asyncio
import logging
import os
from aiogram import Bot, Dispatcher

from handlers.handler_cancel import cancel_router
from handlers.handler_topic_answer_to_client import topic_answer_to_client_router
from handlers.handler_topic_answer import topic_answer_router
from handlers.client_update_info import client_update_info_router
from handlers.administrator_chek_client import administrator_check_client_router
from handlers.administrator_chek_info import administrator_check_info_router
from handlers.administrator_registration_client import add_info_client_router
from handlers.client_registration import client_registration_router
from handlers.start_handler import start_router

logging.basicConfig(level=logging.INFO)

BOT_TOKEN = os.getenv("BOT_TOKEN")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

dp.include_router(start_router)
dp.include_router(cancel_router)
dp.include_router(client_update_info_router)
dp.include_router(add_info_client_router)
dp.include_router(client_registration_router)
dp.include_router(administrator_check_info_router)
dp.include_router(administrator_check_client_router)
dp.include_router(topic_answer_to_client_router)
dp.include_router(topic_answer_router)


async def main():
    logging.info("Бот запущен и готов к работе!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())