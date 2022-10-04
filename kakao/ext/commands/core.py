import asyncio


class Command:
    """
    A class that implements the protocol for a bot text command.

    Parameters:
        name: The name of the command. [type str]
        callback: The coroutine that is executed when the command is called. [type coroutine]
        aliases : The list of aliases the command can be invoked under. [type List[str]|Tuple[str]]
        enabled : A boolean that indicates if the command is currently enabled. [type bool]

    Returns:

    Remarks:
    """

    def __init__(self, func, **kwargs):
        if not asyncio.iscoroutinefunction(func):
            raise TypeError("Callback must be a coroutine.")

        self.name = name = kwargs.get("name") or func.__name__
        if not isinstance(name, str):
            raise TypeError("Name of a command must be a string.")

        self.callback = func
        self.enabled = kwargs.get("enabled", True)
        self.aliases = kwargs.get("aliases", [])

    @property
    def callback(self):
        return self._callback

    @callback.setter
    def callback(self, function):
        self._callback = function

    async def __call__(self, *args, **kwargs):
        return await self.callback(*args, **kwargs)


def command(name=None, cls=None, **attrs):
    if cls is None:
        cls = Command

    def decorator(func):
        if isinstance(func, Command):
            raise TypeError("Callback is already a command.")
        return cls(func, name=name, **attrs)

    return decorator
