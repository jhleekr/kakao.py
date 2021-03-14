kakao.py
=======
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
    async def onReady(self):
        print("Logged on")
    async def onMessage(self, chat):
        if chat.message == "ping":
            await chat.reply("pong!")
kakao.check_reg("LoginId", "LoginPw")
client = Myclass("LoginId", "LoginPw")
client.run()
```

Thanks to (Forked from)
-------
idev-develop/KakaoBot (Commit 8df8cf3)

License
-------
MIT Licence
