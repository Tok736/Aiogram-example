from aiogram import Router, F
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.filters import StateFilter, Command
from aiogram.fsm.context import FSMContext

from .data import available_food_names, available_food_sizes
from .keyboards import make_row_keyboard
from .states import OrderFoodState

from command_list import CommandList

command_list = CommandList(
    name="Конечный автомат",
    commands=["/food"]
)

router = Router(
    name="Пример конечного автомата"
)

@router.message(
    StateFilter(None), 
    Command("food")
)
async def command_food(
    message: Message,
    state: FSMContext,
):
    ''' Установка состояния 'выбирает еду' '''

    await message.answer(
        text="Выберите блюдо:",
        reply_markup=make_row_keyboard(available_food_names)
    )

    await state.set_state(OrderFoodState.choosing_food_name)

@router.message(
    OrderFoodState.choosing_food_name,
    F.text.in_(available_food_names),
)
async def food_chosen(
    message: Message,
    state: FSMContext,
):
    ''' Выбрана корректная еда '''

    await state.update_data(chosen_food=message.text.lower())

    await message.answer(
        text="Спасибо, теперь выберите размер порции:",
        reply_markup=make_row_keyboard(available_food_sizes)
    )
    await state.set_state(OrderFoodState.choosing_food_size)
    
@router.message(
    OrderFoodState.choosing_food_name
)
async def food_chosen_incorrectly(message: Message):
    await message.answer(
        text="Я не знаю такого блюда. Выберите из списка ниже",
        reply_markup=make_row_keyboard(available_food_names)
    )

@router.message(
    OrderFoodState.choosing_food_size,
    F.text.in_(available_food_sizes),
)
async def food_size_chosen(
    message: Message,
    state: FSMContext,
):
    ''' Выбран корректный размер порции '''

    user_data = await state.get_data()

    await message.answer(
        text=f"Вы выбрали {message.text.lower()} порцию {user_data['chosen_food']}",
        reply_markup=ReplyKeyboardRemove(),
    )

    await state.clear()