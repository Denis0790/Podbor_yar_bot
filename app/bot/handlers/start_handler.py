from aiogram import types, F
from aiogram import Router
from keyboards.keyboards import get_main_menu_kb_for_manager, get_main_menu_kb_for_client

start_router = Router()

ADMIN_IDS = [5289542722, 532858619]

@start_router.message(F.text == "/start")
async def command_start(message: types.Message):
    user_id = message.from_user.id

    welcome_text = (
        "👋 **Добро пожаловать в Подбор запчастей!**\n"
        "Здесь вы можете управлять заказами и просматривать историю обслуживания.\n"
        "Нажмите для регистрации: /registration"
    )
    if user_id in ADMIN_IDS:
        markup = get_main_menu_kb_for_manager()
        await message.answer(
            f"🛠 **Панель менеджера**\n\n{welcome_text}",
            reply_markup=markup,
            parse_mode="Markdown"
        )
    else:
        await message.answer(
            f"👤 **Личный кабинет**\n\n{welcome_text}",
            parse_mode="Markdown"
        )