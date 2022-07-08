import discord
from discord.ext import commands
from utils.commands import slash_command
from discord.commands import ApplicationContext
from config import COLOR, BAD, DEV_ID
import json
import datetime
from pytz import timezone


class Attendance(commands.Cog):
    def __init__(self, bot:commands.Bot):
        self.bot = bot

    @slash_command(name="출첵", description="출석체크를 합니다.")
    async def attend(
        self,
        ctx: ApplicationContext
    ):
        now = datetime.datetime.now(timezone("Asia/Seoul"))
        data = open("attendance.json", "r")
        rdata = json.loads(data.read())
        data.close()
        try:
            if rdata["users"][str(ctx.author.id)][0] == now.strftime("%Y-%m-%d"):
                embed = discord.Embed(title="경고", colour=BAD, description="출석체크는 하루에 한 번만 가능합니다.")
                await ctx.respond(embed=embed)
                return
        except KeyError:
            rdata["users"][str(ctx.author.id)] = [0, 0]
        rdata["users"][str(ctx.author.id)][0] = now.strftime("%Y-%m-%d")
        rdata["users"][str(ctx.author.id)][1] += 1
        wdata = json.dumps(rdata, indent=4)
        open("attendance.json", "w").write(wdata)
        embed = discord.Embed(title="출석체크 성공!", color=COLOR)
        embed.add_field(name="날짜", value=f"{now.year}년 {now.month}월 {now.day}일")
        await ctx.respond(embed=embed)

    @slash_command(name="출첵순위", description="출석체크 순위를 출력합니다.")
    async def attendance_ranking(self, ctx: ApplicationContext):
        data = open("attendance.json", "r")
        userdata:dict = json.loads(data.read())["users"]
        data.close()
        ranking = {}
        for x in range(len(userdata)):
            ranking[list(userdata.keys())[x]] = userdata[list(userdata.keys())[x]][1]
        ranking = sorted(ranking.items(), key=lambda kv: (kv[1], kv[0]), reverse=True)
        desc = ""
        for x in range(10):
            try:
                user:discord.User = await self.bot.fetch_user(ranking[x][0])
                desc += f"{x+1}등: {user.mention}({ranking[x][1]}회)\n"
            except IndexError:
                break
        embed = discord.Embed(title="출석체크 순위", color=COLOR, description=desc)
        await ctx.respond(embed=embed)

    @slash_command(name="attjson")
    async def attendance_json(self, ctx: ApplicationContext):
        if ctx.author.id == DEV_ID:
            data = open("attendance.json", "r")
            rdata = str(json.loads(data.read())).split("'")
            data.close()
            dm = await self.bot.create_dm(await self.bot.fetch_user(DEV_ID))
            await ctx.respond("*DM*")
            await dm.send("\"".join(rdata))


def setup(bot):
    print("attendance.py is loaded")
    bot.add_cog(Attendance(bot))


def teardown():
    print("attendance.py unloaded")
