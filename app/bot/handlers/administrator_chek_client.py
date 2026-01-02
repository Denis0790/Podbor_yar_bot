from aiogram import types, F
from aiogram import Router
from aiogram.fsm.context import FSMContext

from api.api_administrator_check_client import get_client_in_backend
from states.states import SearchClientState

administrator_check_client_router = Router()

@administrator_check_client_router.message(F.text == "/Инфо по клиенту")
@administrator_check_client_router.message(F.text == "/admin_check_client")
async def command_check_client(message: types.Message, state: FSMContext):
    await message.answer("Введите номер телефона, для поиска клиента: ")
    await state.set_state(SearchClientState.waiting_number)

@administrator_check_client_router.message(SearchClientState.waiting_number)
async def search_client(message: types.Message, state: FSMContext):
    phone = message.text.strip()

    if not phone.isdigit() or not (10 <= len(phone) <= 11):
        await message.answer("⚠️ Номер должен состоять минимум из 10 - 11 цифр.")
        return
    await message.bot.send_chat_action(message.chat.id, "find_location")

    result = await get_client_in_backend(phone)

    if isinstance(result, dict) and result.get("name"):
        text = (
            f"✅ **Клиент найден!**\n\n"
            f"👤 **Имя:** {result.get('name')}\n"
            f"📞 **Телефон:** {result.get('number')}\n"
            f"🚗 **VIN:** `{result.get('vin')}`\n"
            f"🆔 **ID TG:** {result.get('id_tg')}"
        )
        await message.answer(text, parse_mode="Markdown")
        await state.clear()
    else:
        await message.answer(f"❌ Клиент {phone} не найден.")
        await state.clear()


