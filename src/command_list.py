class CommandList:
    ''' Класс для хранения списка доступных команд '''

    def __init__(
        self,
        name: str,
        commands: tuple[str],
    ) -> None:
        self.name = name
        self.commands = commands

