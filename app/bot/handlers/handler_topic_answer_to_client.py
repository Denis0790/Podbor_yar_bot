from aiogram import Router, F, types

from api.api_administrator_check_client import get_client_by_id_thread

topic_answer_to_client_router = Router()

GROUP_ID = -1003417045317

@topic_answer_to_client_router.message(F.chat.id == GROUP_ID, F.is_topic_message)
async def forward_to_client(message: types.Message):
    if message.text and message.text.startswith("/"):
        return

    thread_id = message.message_thread_id
    print(thread_id)

    client_data = await get_client_by_id_thread(thread_id)

    if client_data and client_data.get("id_tg"):
        user_id = client_data["id_tg"]
        try:
            await message.copy_to(chat_id=user_id)
        except Exception as e:
            await message.reply(f"⚠️ Сообщение не доставлено. Возможно, клиент заблокировал бота.{e}")
    else:
        pass