from random import randint 
from contextlib import suppress

from aiogram import Router, F
from aiogram.types import (
    Message, 
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    CallbackQuery,
)
from aiogram.filters.command import Command
from aiogram.utils.keyboard import (
    InlineKeyboardBuilder,
)
from aiogram.exceptions import TelegramBadRequest
from aiogram.filters.callback_data import CallbackData

from command_list import CommandList
from bot import bot

command_list = CommandList(
    name="Inline buttons",
    commands=[
        "/inline_url",
        "/random",
        "/matrix",
        "/make_number",
        "/make_fabric_number",
    ]
)

router = Router()

@router.message(Command("inline_url"))
async def command_dish(message: Message):
    ''' Хендлер, возвращающий inline клавиатуру с тремя url кнопками '''

    builder = InlineKeyboardBuilder()

    builder.row(InlineKeyboardButton(
        text="GitHub",
        url="https://github.com",
    ))

    builder.row(InlineKeyboardButton(
        text="Оф. канал телеги",
        url="tg://resolve?domain=telegram",
    ))

    user_id = 5344877899
    # chat_info = await bot.get_chat(user_id)

    # if not chat_info.has_private_forwards:
    builder.row(InlineKeyboardButton(
        text="кс кс",
        url=f"tg://user?id={user_id}"
    ))

    await message.answer(
        "Выберите ссылку",
        reply_markup=builder.as_markup()
    )

@router.message(Command("random"))
async def command_random(message: Message):
    ''' Отправляет сообщений с inline клавиатурой и кнопкой для получения случайного числа '''
    builder = InlineKeyboardBuilder()

    builder.add(InlineKeyboardButton(
        text="Сгенерировать",
        callback_data="random_value",
    ))

    await message.answer(
        "Нажмите на кнопку, чтобы получить случайное число от 1 до 100",
        reply_markup=builder.as_markup()
    )

@router.callback_query(F.data == "random_value")
async def send_random_value(callback: CallbackQuery):
    ''' 
    Хендлер на нажатие инлайн кнопки.  
    show_alert=True  - показывает всплывающее окно
    show_alert=False - показывает небольшой текст посередине экрана 
    '''
    
    await callback.message.answer(str(randint(1, 100)))
    await callback.answer(
        text="Ваше случайное число",
        show_alert=True,
    )


@router.message(Command("matrix"))
async def command_matrix(message: Message):
    ''' Отправка inline клавиатуры с 64 кнопками '''
    builder = InlineKeyboardBuilder()

    for i in range(1, 65):
        builder.add(InlineKeyboardButton(
            text=str(i),
            callback_data=f"matrix_{i}"
        ))

    builder.adjust(8)

    await message.answer(
        "Матрица из 64 чисел",
        reply_markup=builder.as_markup(),
    )

@router.callback_query(F.data.startswith("matrix"))
async def callback_matrix(callback: CallbackQuery):
    ''' Обработка нажатия на inline кнопки из matrix '''

    num = callback.data.split("_")[1]

    await callback.answer(
        text =f"Нажата кнопка {num}"
    )

user_data = {}

def get_keyboard() -> InlineKeyboardMarkup:
    ''' Создает клавиатуру '''

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="-1", callback_data="num_decr"), InlineKeyboardButton(text="+1", callback_data="num_incr")],
            [InlineKeyboardButton(text="подтвердить", callback_data="num_accept")]
        ],
    )

    return keyboard

async def update_number(message: Message, value: int) -> None:
    ''' Обновить число '''

    with suppress(TelegramBadRequest):
        await message.edit_text(
            f"Выберите число {value}",
            reply_markup=get_keyboard(),
        )

@router.message(Command("make_number"))
async def command_make_number(message: Message):
    ''' Создает клавиатуру  ''' 

    user_data[message.from_user.id] = 0

    print(message.from_user.id)

    await message.answer(
        "Выберите число 0",
        reply_markup=get_keyboard(),
    )

@router.callback_query(F.data.startswith("num"))
async def callback_matrix(callback: CallbackQuery):
    ''' Обработка нажатия на inline кнопки из matrix '''

    command = callback.data.split("_")[1]

    value = user_data[callback.from_user.id]

    if command == "incr":
        value += 1
        await update_number(callback.message, value)
    elif command == "decr":
        value -= 1
        await update_number(callback.message, value)
    elif command == "accept":
        print("Подтверждение")
        await callback.message.edit_text(f"Подтверждено число {value}")

    user_data[callback.from_user.id] = value

    await callback.answer(
        text=f"Новое число {value}"
    )




class NumberCallbackFactory(CallbackData, prefix="fabric_num"):
    action: str
    value: int | None = None

def get_fabric_keyboard():
    ''' Создает клавиатуру для примера с фабричным коллбеком '''

    builder = InlineKeyboardBuilder()

    builder.button(
        text="-2",
        callback_data=NumberCallbackFactory(action="change", value=-2),
    )
    builder.button(
        text="-1",
        callback_data=NumberCallbackFactory(action="change", value=-1),
    )
    builder.button(
        text="+1",
        callback_data=NumberCallbackFactory(action="change", value=+1),
    )
    builder.button(
        text="+2",
        callback_data=NumberCallbackFactory(action="change", value=+2),
    )
    builder.button(
        text="Подтвердить", 
        callback_data=NumberCallbackFactory(action="accept")
    )

    builder.adjust(4)

    return builder.as_markup()

@router.message(Command("make_fabric_number"))
async def command_make_fabric_number(message: Message):
    ''' Отправляет сообщение с фабричными кнопками '''

    user_data[message.from_user.id] = 0

    await message.answer(
        "Ваше число 0",
        reply_markup=get_fabric_keyboard(),
    )

async def update_number_fabric(message: Message, value: int):
    ''' Редактирует сообщение '''

    with suppress(TelegramBadRequest):
        await message.edit_text(
            f"Ваше число {value}",
            reply_markup=get_fabric_keyboard(),
        )

@router.callback_query(NumberCallbackFactory.filter(F.action == "change"))
async def callback_num_change(
    callback: CallbackQuery,
    callback_data: NumberCallbackFactory,
):
    ''' Изменяем число '''

    user_data[callback.from_user.id] += callback_data.value

    await update_number_fabric(
        callback.message, 
        user_data[callback.from_user.id]
    )

    await callback.answer()

@router.callback_query(NumberCallbackFactory.filter(F.action == "accept"))
async def callback_num_accept(
    callback: CallbackQuery,
    callback_data: NumberCallbackFactory,
):
    ''' Подтверждаем число '''

    value = user_data[callback.from_user.id]
    await callback.message.edit_text(
        text=f"Число подтверждено {value}"
    )
    await callback.answer()