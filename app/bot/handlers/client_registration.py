from aiogram import types, F
from aiogram import Router
from aiogram.fsm.context import FSMContext

from states.states import RegistrationClientState

from api.api_registration_client import registration_client
from data.data_registration_client import DataRegistrationClient

client_registration_router = Router()

GROUP_ID = -1003417045317

@client_registration_router.message(F.text == "/registration")
async def command_client_registration(message: types.Message, state: FSMContext):
    await message.answer("🤝 Рад Вас видеть! Что бы наше общение проходило предметно и по делу - давайте"
                         "пройдём небольшую регистрацию.\nВведите пожалуйста Ваше имя:")
    await state.set_state(RegistrationClientState.waiting_name)


@client_registration_router.message(RegistrationClientState.waiting_name)
async def process_name(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text.strip())
    await message.answer("📱 Теперь введите Ваш номер телефона:")
    await state.set_state(RegistrationClientState.waiting_number)


@client_registration_router.message(RegistrationClientState.waiting_number)
async def process_number(message: types.Message, state: FSMContext):
    number = "".join(filter(str.isdigit, message.text))

    if not (10 <= len(number) <= 11):
        await message.answer("⚠️ Неверный формат. Попробуйте еще раз:")
        return

    await state.update_data(number=number)
    await message.answer("🚗 И последнее: введите VIN вашего автомобиля (17 символов):")
    await state.set_state(RegistrationClientState.waiting_vin)


@client_registration_router.message(RegistrationClientState.waiting_vin)
async def process_vin(message: types.Message, state: FSMContext):
    vin = message.text.strip().upper()

    if len(vin) != 17:
        await message.answer(
            f"⚠️ **Ошибка в VIN-коде!**\n\n"
            f"VIN должен содержать ровно **17** символов.\n"
            f"Вы ввели: `{len(vin)}`.\n\n"
            f"Пожалуйста, проверьте и пришлите корректный код:"
        )
        return

    user_data = await state.get_data()
    name = user_data['name']
    number = user_data['number']

    try:
        topic = await message.bot.create_forum_topic(
            chat_id=GROUP_ID,
            name=f"{name} | {number}"
        )
        thread_id = topic.message_thread_id
    except Exception as e:
        print(f"Ошибка при создании темы: {e}")
        thread_id = 0

    reg_data = DataRegistrationClient(
        id_tg=message.from_user.id,
        name=name,
        number=number,
        vin=vin,
        id_thread=thread_id
    )

    await message.bot.send_chat_action(message.chat.id, "typing")

    result = await registration_client(reg_data)

    if result["success"]:
        if thread_id != 0:
            await message.bot.send_message(
                chat_id=GROUP_ID,
                message_thread_id=thread_id,
                text=f"🆕 **Новая регистрация!**\n\n👤 Имя: {name}\n📞 Тел: {number}\n🚗 VIN: `{vin}`", parse_mode="Markdown"
            )

        text = (
            "✅ **Регистрация прошла успешно!**\n\n"
            f"👤 **Имя:** {reg_data.name}\n"
            f"📞 **Номер:** {reg_data.number}\n"
            f"🚗 **VIN:** `{reg_data.vin}`\n"
        )

        await message.answer(text, parse_mode="Markdown")
        await state.clear()
    else:
        await message.answer(f"❌ Ошибка регистрации: {result['message']}")