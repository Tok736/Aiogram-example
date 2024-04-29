from aiogram import Router, F
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from command_list import CommandList

command_list = CommandList(
    name="Общие хендлеры",
    commands=["/cancel"],
)

router = Router()

@router.message(Command("cancel"))
@router.message(F.text.lower() == "отмена")
async def command_cancel(
    message: Message,
    state: FSMContext
):
    ''' Очистка состояния и очистка клавиатуры '''

    await state.clear()
    await message.answer(
        text="Действие отменено",
        reply_markup=ReplyKeyboardRemove(),
    )