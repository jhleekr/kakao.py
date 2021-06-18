import kakao
from kakao.ext import commands
from kakao.ext.commands import Bot


@commands.command()
async def ping(ctx):
    await ctx.reply("pong")
    return


kakao.check_reg("LoginId", "LoginPw")
bot = Bot("hey ", LoginId="LoginId", LoginPw="LoginPw")
bot.add_command(ping)
bot.run()
