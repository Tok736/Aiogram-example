from aiogram import Router, F
from aiogram.types import (
    Message, 
    KeyboardButton, 
    ReplyKeyboardMarkup, 
    ReplyKeyboardRemove,
    KeyboardButtonPollType,
    KeyboardButtonRequestUser,
    KeyboardButtonRequestChat,
)
from aiogram.filters.command import Command
from aiogram.utils.keyboard import (
    ReplyKeyboardBuilder,
)

from command_list import CommandList


command_list = CommandList(
    name="Buttons",
    commands=[
        "/dish",
        "/reply_builder",
        "/special_buttons",
    ]
)

router = Router()

@router.message(Command("dish"))
async def command_dish(message: Message):
    ''' Хендлер, возвращающий клавиатуру с двумя кнопками '''
    buttons = [
        [
            KeyboardButton(text="С пюрешкой"),
            KeyboardButton(text="Без пюрешки"),
        ],
    ]
    keyboard = ReplyKeyboardMarkup(
        keyboard=buttons,
        resize_keyboard=True,
        input_field_placeholder="Выберите способ подачи"
    )
    await message.answer("Как подавать котлеты?", reply_markup=keyboard)

@router.message(F.text.lower() == "с пюрешкой")
async def with_puree(message: Message):
    ''' Хендлер для обработки нажатия на кнопку "С пюрешкой" '''

    await message.reply(
        "Отличный выбор",
        reply_markup=ReplyKeyboardRemove()
    )

@router.message(F.text.lower() == "без пюрешки")
async def with_puree(message: Message):
    ''' Хендлер для обработки нажатия на кнопку "Без пюрешки" '''

    await message.reply(
        "Так же не вкусно",
        reply_markup=ReplyKeyboardRemove()
    )

@router.message(Command("reply_builder"))
async def command_reply_builder(message: Message):
    ''' Построение кнопок с помощью билдера ReplyKeyboardBuilder '''
    builder = ReplyKeyboardBuilder()
    for i in range(1, 17):
        builder.add(
            KeyboardButton(text=str(i))
        )
    
    builder.adjust(4)
    await message.answer(
        "Выберите число: ",
        reply_markup=builder.as_markup(
            resize_keyboard=True,
            input_field_placeholder="Выберите число: ",
        )
    )

@router.message(Command("special_buttons"))
async def command_special_buttons(message: Message):
    ''' Специальные кнопки '''
    builder = ReplyKeyboardBuilder()

    builder.row(
        KeyboardButton(text="Геолокация", request_location=True),
        KeyboardButton(text="Контакт", request_contact=True),
    )

    builder.row(
        KeyboardButton(
            text="Викторина",
            request_poll=KeyboardButtonPollType(type="quiz")
        )
    )

    builder.row(
        KeyboardButton(
            text="Премиум пользователь",
            request_user=KeyboardButtonRequestUser(
                request_id=1,
                user_is_premium=True,
            )
        ),
        KeyboardButton(
            text="Выбрать супергруппу с форумами",
            request_chat=KeyboardButtonRequestChat(
                request_id=2,
                chat_is_channel=False,
                chat_is_forum=True,
            )
        )
    )

    await message.answer(
        "Выберите действие: ",
        reply_markup=builder.as_markup(resize_keyboard=True),
    )
    

@router.message(F.user_shared)
async def on_user_shared(message: Message):
    ''' Обработка отправленного пользователя '''

    await message.answer(
        f"Вы отправили: \n"
        f"Request: {message.user_shared.request_id}\n"
        f"User ID: {message.user_shared.user_id}"
    )

@router.message(F.chat_shared)
async def on_chat_shared(message: Message):
    ''' Обработка отправленной группы '''

    await message.answer(
        f"Вы отправили: \n"
        f"Request: {message.chat_shared.request_id}\n"
        f"User ID: {message.chat_shared.chat_id}"
    )

