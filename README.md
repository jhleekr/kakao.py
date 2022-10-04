kakao.py
=======
[![pypi](https://img.shields.io/pypi/v/kakao.py.svg)](https://pypi.python.org/pypi/kakao.py)

kakao.py is a very simple kakaotalk LOCO/HTTP API protocol wrapper for python.

Introduction
------------
Loco protocol compatible python library

This is discord.py style rewritten version of KakaoBot.

DO NOT USE IN ABUSING. ABUSING CAN CAUSE PERMANENT SERVICE RESTRICTION.

Quick Start
-------
```python
import kakao

class Myclass(kakao.Client):
    async def on_ready(self):
        print("Logged on")
    async def on_message(self, chat):
        if chat.message == "ping":
            await chat.reply("pong!")
            
kakao.check_reg("LoginId", "LoginPw")
client = Myclass("LoginId", "LoginPw")
client.run()
```

Quick Start (Bot)
-------
```python
import kakao
from kakao.ext import commands
from kakao.ext.commands import Bot


@commands.command()
async def ping(ctx):
    await ctx.reply("pong")
    return


kakao.check_reg("LoginId", "LoginPw")
bot = Bot("/", LoginId="LoginId", LoginPw="LoginPw")
bot.add_command(ping)
bot.run()
```

Thanks to (Forked from)
-------
ksaidev/KakaoBot (Commit 8df8cf3)

License
-------
MIT Licence
