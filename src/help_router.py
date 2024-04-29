from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.utils.formatting import as_list, Bold, as_marked_section

from command_list import CommandList

from message_work.examples import command_list as message_command_list
from state_machine.router  import command_list as state_command_list
from common.router         import command_list as common_command_list

router = Router(
    name="Роутер для команды /help"
)

@router.message(Command("help"))
async def command_help(message: Message):
    ''' Отправка все доступных команд '''
    all_commands: list[CommandList] = [
        message_command_list, 
        state_command_list,
        common_command_list,
    ]

    content = as_list(
        as_marked_section(
            Bold("Доступные команды:"),
            "/help",
            marker="  ",
        ),
        *(
            as_marked_section(
                Bold(command_list.name),
                *command_list.commands,
                marker="  ",
            ) for command_list in all_commands
        ),
        sep="\n",
    )

    await message.answer(**content.as_kwargs())
