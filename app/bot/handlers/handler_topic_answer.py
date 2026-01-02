from aiogram import types, F
from aiogram import Router

from api.api_administrator_check_client import get_client_by_tg_id

topic_answer_router = Router()

GROUP_ID = -1003417045317

@topic_answer_router.message()
async def handle_all_messages(message: types.Message):
    client_data = await get_client_by_tg_id(message.from_user.id)

    if client_data is None:
        await message.answer("Вы еще не зарегистрированы. Нажмите /registration")
        return

    thread_id = client_data.get("id_thread")
    if not thread_id:
        await message.answer("Ваша заявка еще обрабатывается, скоро менеджер создаст чат.")
        return

    await message.copy_to(chat_id=GROUP_ID, message_thread_id=thread_id)