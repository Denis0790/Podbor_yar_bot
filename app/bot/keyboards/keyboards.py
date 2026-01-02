from aiogram.utils.keyboard import ReplyKeyboardBuilder

def get_main_menu_kb_for_manager():
    builder = ReplyKeyboardBuilder()

    builder.button(text="/Инфо по клиенту")
    builder.button(text="/История заказов")
    builder.button(text="/Добавить заказ")
    builder.button(text="/Изменить свои данные")

    builder.adjust(2)

    return builder.as_markup(
        resize_keyboard=True,
        is_persistent=True
    )


def get_main_menu_kb_for_client():
    builder = ReplyKeyboardBuilder()

    builder.button(text="/Изменить свои данные")

    return builder.as_markup(
        resize_keyboard=True,
        is_persistent=True
    )