import logging

from aiogram import types, F
from aiogram import Router
from aiogram.fsm.context import FSMContext

from states.states import SearchInfoState

from api.api_administrator_search_order import get_info_in_backend

administrator_check_info_router = Router()


@administrator_check_info_router.message(F.text == "/История заказов")
@administrator_check_info_router.message(F.text == "/check_info")
async def command_check_info(message: types.Message, state: FSMContext):
    await message.answer("Для поиска инфо по клиенту, введите его номер телефона: ")
    await state.set_state(SearchInfoState.waiting_number)

@administrator_check_info_router.message(SearchInfoState.waiting_number, F.text)
async def command_check_info_wait(message: types.Message, state: FSMContext):
    print(f"DEBUG: Хэндлер сработал! Текст: {message.text}")
    phone = message.text.strip()

    if not phone.isdigit() or not (10 <= len(phone) <= 11):
        await message.answer("⚠️ Номер должен состоять из 10-11 цифр.")
        return

    await message.bot.send_chat_action(
        chat_id=message.chat.id,
        action="find_location",
        message_thread_id=message.message_thread_id
    )

    result = await get_info_in_backend(phone)

    if isinstance(result, list) and len(result) > 0:
        descriptions = [f"• {item.get('description', '—')}" for item in result]
        all_info = "\n".join(descriptions)

        text = (
            f"✅ **Информация найдена!**\n"
            f"📞 **Номер:** `{phone}`\n\n"
            f"📝 **История:**\n{all_info}"
        )
        try:
            await message.answer(text)
        except Exception as e:
            logging.error(f"Ошибка HTML-парсинга: {e}")
            await message.answer(text, parse_mode=None)
        await state.clear()
    else:
        await message.answer(f"❌ По номеру {phone} ничего не найдено.")
        await state.clear()