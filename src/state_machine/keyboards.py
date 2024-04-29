from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def make_row_keyboard(items: list[str]) -> ReplyKeyboardMarkup:
    ''' Создает однострочную клавиатуру '''

    keyboard = [KeyboardButton(text=item) for item in items]

    return ReplyKeyboardMarkup(
        keyboard=[keyboard],
        resize_keyboard=True,
    )


