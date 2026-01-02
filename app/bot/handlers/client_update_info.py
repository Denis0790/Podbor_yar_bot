from aiogram import types, F
from aiogram import Router
from aiogram.fsm.context import FSMContext
from states.states import UpdateInfoState
from api.api_update_client import update_client
from data.data_registration_client import DataUpdateClient

client_update_info_router = Router()


@client_update_info_router.message(F.text == "/Изменить свои данные")
@client_update_info_router.message(F.text == "/update_reg")
async def command_client_update_reg(message: types.Message, state: FSMContext):
    await message.answer("Давайте обновим Ваши данные, \nвведите пожалуйста Ваше имя: ")
    await state.set_state(UpdateInfoState.waiting_name)

@client_update_info_router.message(UpdateInfoState.waiting_name)
async def process_name(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text.strip())
    await message.answer("📱 Теперь введите Ваш номер телефона:")
    await state.set_state(UpdateInfoState.waiting_number)

@client_update_info_router.message(UpdateInfoState.waiting_number)
async def process_number(message: types.Message, state: FSMContext):
    number = "".join(filter(str.isdigit, message.text))

    if not (10 <= len(number) <= 11):
        await message.answer("⚠️ Неверный формат. Попробуйте еще раз:")
        return

    await state.update_data(number=number)
    await message.answer("🚗 И последнее: введите VIN вашего автомобиля (17 символов):")
    await state.set_state(UpdateInfoState.waiting_vin)


@client_update_info_router.message(UpdateInfoState.waiting_vin)
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
    update_data = DataUpdateClient(
        name=user_data.get("name"),
        number=user_data.get("number"),
        vin=vin
    )

    result = await update_client(id_tg=message.from_user.id, up_client=update_data)

    if result.get("success"):
        await message.answer("✅ Данные успешно обновлены!")
        await state.clear()
    else:
        await message.answer(f"❌ Произошла ошибка: {result.get('message')}")
