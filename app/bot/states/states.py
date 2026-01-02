from aiogram.fsm.state import StatesGroup, State

class SearchClientState(StatesGroup):
    waiting_number = State()

class SearchInfoState(StatesGroup):
    waiting_number = State()

class RegistrationClientState(StatesGroup):
    waiting_name = State()
    waiting_number = State()
    waiting_vin = State()

class InfoClientState(StatesGroup):
    waiting_number = State()
    waiting_info = State()

class UpdateInfoState(StatesGroup):
    waiting_name = State()
    waiting_number = State()
    waiting_vin = State()