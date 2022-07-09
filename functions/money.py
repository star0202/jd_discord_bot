import discord
from discord.ext import commands
from utils.commands import slash_command
from utils.gettime import get_time
from discord.commands import ApplicationContext, Option
from config import COLOR, BAD, DEV_ID, DB_CHANNEL_ID
import random
import json


class Money(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @slash_command(name="지원금")
    async def money_give(self, ctx: ApplicationContext):
        now = get_time()
        db_channel = await self.bot.fetch_channel(DB_CHANNEL_ID)
        db_pins = await db_channel.pins()
        db = db_pins[1]
        data = json.loads(db.content)
        try:
            if data["users"][str(ctx.author.id)][0] == now.strftime("%Y-%m-%d"):
                embed = discord.Embed(title="경고", colour=BAD, description="지원금 수령은 하루에 한 번만 가능합니다.")
                await ctx.respond(embed=embed)
                return
        except KeyError:
            data["users"][str(ctx.author.id)] = [0, 0]
        given_money = random.choice([100, 100, 100, 100, 100, 500, 500, 500, 500, 1000, 1000, 1000, 2000, 2000, 5000])
        data["users"][str(ctx.author.id)][0] = now.strftime("%Y-%m-%d")
        data["users"][str(ctx.author.id)][1] += given_money
        my_money = data["users"][str(ctx.author.id)][1]
        await db.edit("\"".join(str(data).split("'")))
        embed = discord.Embed(title="수령 성공!", color=COLOR)
        embed.add_field(name="수령한 금액", value=f"{given_money}원")
        embed.add_field(name="현재 통장", value=f"{my_money}원")
        await ctx.respond(embed=embed)

    @slash_command(name="moneyedit")
    async def attendance_edit(self, ctx: ApplicationContext, jsondata: Option(str)):
        if ctx.author.id == DEV_ID:
            db_channel = await self.bot.fetch_channel(DB_CHANNEL_ID)
            db_pins = await db_channel.pins()
            db = db_pins[1]
            await db.edit(jsondata)
            await ctx.respond("Done")




def setup(bot):
    print("money.py is loaded")
    bot.add_cog(Money(bot))


def teardown():
    print("money.py unloaded")
