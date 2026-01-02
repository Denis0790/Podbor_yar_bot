from aiogram import types, F
from aiogram.fsm.context import FSMContext
from aiogram import Router

from keyboards.keyboards import get_main_menu_kb_for_client

cancel_router = Router()

@cancel_router.message(F.text == "/отмена")
@cancel_router.message(F.text == "/cancel")
async def cancel_handler(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return

    await state.clear()
    await message.answer(
        "Действие отменено. Возвращаюсь в главное меню.",
        reply_markup=get_main_menu_kb_for_client()
    )