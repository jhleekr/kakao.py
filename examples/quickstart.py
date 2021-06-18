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
