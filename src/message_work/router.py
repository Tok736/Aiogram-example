from datetime import datetime

from aiogram import Router, html, F
from aiogram.types import Message
from aiogram.filters.command import Command, CommandObject, CommandStart
from aiogram.enums import ParseMode
from aiogram.utils.formatting import (
    Text, Bold, as_list, as_marked_section, as_key_value, HashTag
)

from command_list import CommandList

router = Router(
    name="Примеры работы с текстом"
)

command_list = CommandList(
    name="Работа с текстом: ",
    commands=[
        "/start",
        "/reply",
        "/dice",
        "/parse_mode",
        "/hello_user",
        "/marked_sections",
        "/format_save",
        "/get_entities",
        "/set_timer",
        "/generate_deeplink"
    ],
)


@router.message(Command("reply"))
async def command_reply(message: Message):
    ''' Reply отправляет ответ на конкретное сообщение '''
    await message.reply("Сообщение с ответом")

@router.message(Command("dice"))
async def command_dice(message: Message):
    ''' Отправка особого сообщения (с игральными костями) '''
    await message.answer_dice(emoji="🎲")
    await message.answer_dice(emoji="🎯")
    await message.answer_dice(emoji="🏀")
    await message.answer_dice(emoji="⚽")
    await message.answer_dice(emoji="🎳")
    await message.answer_dice(emoji="🎰")

@router.message(Command("parse_mode"))
async def command_parse_mode(message: Message):
    '''
    Отправка сообщения с какой-либо разметкой. 
    Для задания разметки по всему проекту используется:

    bot = Bot(token=TOKEN, parse_mode=ParseMode.HTML)
    '''

    await message.answer(
        "Сообщение с <b>HTML разметкой</b>!",
        parse_mode=ParseMode.HTML
    )
    await message.answer(
        "Сообщение с *MarkdownV2 разметкой*",
        parse_mode=ParseMode.MARKDOWN_V2
    )
    await message.answer(
        "Сообщение без разметки",
        parse_mode=None
    )

@router.message(Command("hello_user"))
async def command_hello(message: Message):
    ''' Экранирование информации, чувствительной к выбранной разметке. Получение имени пользователя '''
    content = Text(
        "Hello, ",
        Bold(message.from_user.full_name)
    )
    await message.answer(**content.as_kwargs())

@router.message(Command("marked_sections"))
async def command_marked_sections(message: Message):
    ''' Хендлер, демонстрирующий комплексное использование форматирования '''

    content = as_list(
        as_marked_section(
            Bold("Success:"),
            "Test 1",
            "Test 2",
            "Test 4",
            marker="✅ ",
        ),
        as_marked_section(
            Bold("Failed:"),
            "Test 3",
            "Test 5",
            marker="❌ ",
        ),
        as_marked_section(
            Bold("Summary:"),
            as_key_value("Total", 5),
            as_key_value("Success", 3),
            as_key_value("Failed", 2),
            marker="   ",
        ),
        HashTag("#test"),
        sep="\n\n",
    )
    await message.answer(**content.as_kwargs())

@router.message(Command("format_save"))
async def command_format_save(message: Message):
    ''' Способ сохранить исходное форматирование, которое отправил пользователь '''

    time_now = datetime.now().strftime("%H:%M")
    time_now = html.underline(time_now)

    await message.answer(
        f"{message.html_text}\n\n{time_now}",
        parse_mode=ParseMode.HTML
    )

@router.message(Command("get_entities"))
async def command_get_entities(message: Message):
    ''' Получение сущностей из сообщения (например, паролей, почт, сайтов и т.д.) '''
    
    data = []

    entities = message.entities or []
    for item in entities:
        data.append((
            item.type, 
            item.extract_from(message.text),
        ))
    
    content = as_list(
        *(
            f"{item[0]}: {item[1]}" for item in data
        ),
        sep="\n\n",
    )

    await message.answer(**content.as_kwargs())

@router.message(Command("set_timer"))
async def command_set_timer(
    message: Message,
    command: CommandObject,
):
    ''' Получение аргументов для команды '''

    args = command.args

    if not args or len(args.split()) != 2:
        await message.answer(
            "Использование команды: /set_timer <time> <message>"
        )
        return

    delay_time, message_text = args.split()

    await message.answer(
        "Таймер добавлен!\n"
        f"Время: {delay_time}\n"
        f"Текст: {message_text}"
    )

@router.message(CommandStart(
    deep_link=True,
))
async def command_start_with_token(
    message: Message,
    command: CommandObject,
):
    ''' Использование диплинков '''
    token = command.args
    await message.answer(
        "Вы отправили диплинк с токеном:\n"
        f"token: {token}"
    )

@router.message(CommandStart(
    deep_link=False
))
async def command_start(message: Message):
    ''' Обработка команд. answer отправляет сообщение в тот же чат '''
    await message.answer("Hello! Input /help")

@router.message(Command("generate_deeplink"))
async def command_generate_deeplink(message: Message):
    ''' Генерация диплинка '''
    await message.answer(
        "t.me/test_athena_telegram_bot?start=DSFIJJdsajfiafd"
    )

@router.message(F.sticker)
async def echo_gif(message: Message):
    ''' 
    file_id - многоразовый id (хранится на сервер) 
    file_unique_id - одноразовый id
    '''
    await message.reply_sticker(message.sticker.file_id)