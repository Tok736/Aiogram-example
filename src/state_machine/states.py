from aiogram.fsm.state import State, StatesGroup

class OrderFoodState(StatesGroup):
    choosing_food_name = State()
    choosing_food_size = State()

