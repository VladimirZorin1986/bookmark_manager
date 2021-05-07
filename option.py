import commands
import typing as t


class Option:

    def __init__(self, name: str,
                 command: commands.Command,
                 prep_call: t.Optional[t.Callable] = None) -> None:
        self.name = name
        self.command = command
        self.prep_call = prep_call

    def choose(self):
        data = self.command.execute(self.prep_call()) if self.prep_call else self.command.execute()
        print(data)

    def __str__(self):
        return self.name
