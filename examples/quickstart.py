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
