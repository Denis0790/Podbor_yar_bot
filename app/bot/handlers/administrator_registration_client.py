from datetime import datetime
from aiogram import types, F
from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram import html
from states.states import InfoClientState
from api.api_add_info import add_info

add_info_client_router = Router()


@add_info_client_router.message(F.text == "/Добавить заказ")
@add_info_client_router.message(F.text == "/add_info_client")
async def command_add_info_client(message: types.Message, state: FSMContext):
    await message.answer("Введи номер телефона к кому хочешь привязать историю заказа: ")
    await state.set_state(InfoClientState.waiting_number)

@add_info_client_router.message(InfoClientState.waiting_number)
async def processed_number(message: types.Message, state: FSMContext):
    await state.update_data(number=message.text.strip())
    await message.answer("Теперь сам текст: ")
    await state.set_state(InfoClientState.waiting_info)


@add_info_client_router.message(InfoClientState.waiting_info)
async def processed_info(message: types.Message, state: FSMContext):
    info_text = message.text.strip()
    user_data = await state.get_data()
    phone_number = user_data.get("number")

    current_date = datetime.now().strftime("%d.%m.%Y")
    safe_info = html.quote(info_text)
    formatted_text = (
        f"🗓 **Запись от {current_date}**\n"
        f"───────────────────\n"
        f"{safe_info}\n"
        f"───────────────────"
    )

    result = await add_info(number=phone_number, info=formatted_text)

    if result.get("success"):
        await message.answer(f"✅ Инфо привязана к номеру {phone_number}!")
        await state.clear()
    else:
        await message.answer(f"❌ Ошибка: {result.get('message')}")