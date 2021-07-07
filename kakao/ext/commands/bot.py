import kakao
import traceback
import sys
import asyncio
from socket import socket
from .core import Command

"""
The MIT License (MIT)
Copyright (c) 2015-present Rapptz
"""


class _CaseInsensitiveDict(dict):
    def __contains__(self, k):
        return super().__contains__(k.casefold())

    def __delitem__(self, k):
        return super().__delitem__(k.casefold())

    def __getitem__(self, k):
        return super().__getitem__(k.casefold())

    def get(self, k, default=None):
        return super().get(k.casefold(), default)

    def pop(self, k, default=None):
        return super().pop(k.casefold(), default)

    def __setitem__(self, k, v):
        super().__setitem__(k.casefold(), v)


class CommandRegistrationError(Exception):
    """
    An exception raised when the command can't be added

    Parameters:
        name: The command name that had the error. [type str]
        alias_conflict: Whether the name that conflicts is an alias of the command we try to add. [type bool]

    Returns:

    Remarks:
    """

    def __init__(self, name, *, alias_conflict=False):
        self.name = name
        self.alias_conflict = alias_conflict
        type_ = "alias" if alias_conflict else "command"
        super().__init__(f"The {type_} {name} is already an existing command or alias.")


class BotBase:
    def __init__(
        self,
        command_prefix,
        **kwargs,
    ):
        case_insensitive = kwargs.get("case_insensitive", False)
        self.all_commands = _CaseInsensitiveDict() if case_insensitive else {}
        self.case_insensitive = case_insensitive
        self.command_prefix = command_prefix
        if not isinstance(self.command_prefix, str):
            if not (
                isinstance(self.command_prefix, list)
                and all(isinstance(x, str) for x in self.command_prefix)
            ):
                raise TypeError()
        super().__init__(**kwargs)

    def find_prefix(self, msg):
        if isinstance(self.command_prefix, str):
            orig = [self.command_prefix]
        else:
            orig = self.command_prefix
        for i in orig:
            if msg.startswith(i):
                return msg[len(i) :]
        return None

    async def on_command_error(self, msg, exception):
        print(f"Ignoring exception in command {msg}:", file=sys.stderr)
        traceback.print_exception(
            type(exception), exception, exception.__traceback__, file=sys.stderr
        )

    def add_command(self, command):
        if not isinstance(command, Command):
            raise TypeError("The command passed must be a subclass of Command")

        if isinstance(self, Command):
            command.parent = self

        if command.name in self.all_commands:
            raise CommandRegistrationError(command.name)

        self.all_commands[command.name] = command
        for alias in command.aliases:
            if alias in self.all_commands:
                self.remove_command(command.name)
                raise CommandRegistrationError(alias, alias_conflict=True)
            self.all_commands[alias] = command

    def remove_command(self, name):
        command = self.all_commands.pop(name, None)

        # does not exist
        if command is None:
            return None

        if name in command.aliases:
            # we're removing an alias so we don't want to remove the rest
            return command

        # we're not removing the alias so let's delete the rest of them.
        for alias in command.aliases:
            cmd = self.all_commands.pop(alias, None)
            # in the case of a CommandRegistrationError, an alias might conflict
            # with an already existing command. If this is the case, we want to
            # make sure the pre-existing command is not removed.
            if cmd not in (None, command):
                self.all_commands[alias] = cmd
        return command

    async def _process(self, chat):
        msg = chat.message
        cmd = self.find_prefix(msg)
        if cmd is None:
            return
        for x, y in self.all_commands.items():
            if cmd.startswith(x):
                await y(chat)
                return
        return

    async def invoke(self, chat):
        try:
            await self._process(chat)
        except Exception as e:
            await self.on_command_error(chat.message, e)

    async def process_commands(self, chat):
        await chat.read()
        await self.invoke(chat)

    async def on_message(self, chat):
        await self.process_commands(chat)

    async def on_ready(self):
        print("Logged on")


class Bot(BotBase, kakao.Client):
    """
    Represents a kakaotalk bot.

    Parameters:
        command_prefix: The command prefix is what the message content must contain initially to have a command invoked. [type str|List[str]]
        case_insensitive: Whether the commands should be case insensitive. [type bool]
        LoginId: account ID [type str]
        LoginPw: account PW [type str]
        device_name : Device's Name. [type str]
        device_uuid : Device's Uuid. [type str]

    Returns:

    Remarks:
    """

    pass