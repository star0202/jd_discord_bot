import discord
import dotenv
from discord.ext import commands
from utils.commands import slash_command
from utils.gettime import get_time
from discord.commands import ApplicationContext, Option
from config import COLOR, BAD, DEV_ID
import json
import os
import logging

logger = logging.getLogger(__name__)
dotenv.load_dotenv(".env")


class Attendance(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @slash_command(name="출첵", description="출석체크를 합니다.")
    async def attend(
        self,
        ctx: ApplicationContext
    ):
        now = get_time()
        db_channel = await self.bot.fetch_channel(os.getenv("DB_CHANNEL_ID"))
        db_pins = await db_channel.pins()
        db = db_pins[0]
        data = json.loads(db.content)
        try:
            if data["users"][str(ctx.author.id)][0] == now.strftime("%Y-%m-%d"):
                embed = discord.Embed(title="경고", colour=BAD, description="출석체크는 하루에 한 번만 가능합니다.")
                await ctx.respond(embed=embed)
                return
        except KeyError:
            data["users"][str(ctx.author.id)] = [0, 0]
        data["users"][str(ctx.author.id)][0] = now.strftime("%Y-%m-%d")
        data["users"][str(ctx.author.id)][1] += 1
        await db.edit("\"".join(str(data).split("'")))
        embed = discord.Embed(title="출석체크 성공!", color=COLOR)
        embed.add_field(name="날짜", value=f"{now.year}년 {now.month}월 {now.day}일")
        await ctx.respond(embed=embed)

    @slash_command(name="출첵순위", description="출석체크 순위를 출력합니다.")
    async def attendance_ranking(self, ctx: ApplicationContext):
        db_channel = await self.bot.fetch_channel(os.getenv("DB_CHANNEL_ID"))
        db_pins = await db_channel.pins()
        db = db_pins[0]
        data = json.loads(db.content)
        userdata: dict = data["users"]
        ranking = {}
        for x in range(len(userdata)):
            ranking[list(userdata.keys())[x]] = userdata[list(userdata.keys())[x]][1]
        ranking = sorted(ranking.items(), key=lambda kv: (kv[1], kv[0]), reverse=True)
        desc = ""
        for x in range(10):
            try:
                user: discord.User = await self.bot.fetch_user(ranking[x][0])
                desc += f"{x+1}등: {user.mention}({ranking[x][1]}회)\n"
            except IndexError:
                break
        embed = discord.Embed(title="출석체크 순위", color=COLOR, description=desc)
        await ctx.respond(embed=embed)

    @slash_command(name="attedit")
    async def attendance_edit(self, ctx: ApplicationContext, jsondata: Option(str)):
        if ctx.author.id == DEV_ID:
            db_channel = await self.bot.fetch_channel(os.getenv("DB_CHANNEL_ID"))
            db_pins = await db_channel.pins()
            db = db_pins[0]
            await db.edit(jsondata)
            await ctx.respond("Done")


def setup(bot):
    logger.info("Loaded")
    bot.add_cog(Attendance(bot))


def teardown():
    logger.info("Unloaded")
