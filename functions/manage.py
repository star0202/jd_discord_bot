import discord
from discord.ext import commands
from utils.commands import slash_command
from discord.commands import ApplicationContext
from config import color
import time


class Manage(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @slash_command(name="핑", description="봇의 핑을 전송합니다.")
    async def ping(self, ctx:ApplicationContext):
        embed = discord.Embed(title=":ping_pong: 퐁!", color=color)
        embed.add_field(
            name="discord API Ping: ", value=f"{round(ctx.bot.latency * 1000)} ms"
        )
        await ctx.respond(embed=embed)

    @slash_command(name="봇", description="봇의 정보를 전송합니다.")
    async def botinfo(self, ctx:ApplicationContext):
        nowtime = time.time()
        s = round(nowtime - self.bot.start_time)
        d = 0
        h = 0
        m = 0
        while s >= 86400:
            s = s - 86400
            d += 1
        while s >= 3600:
            s = s - 3600
            h += 1
        while s >= 60:
            s = s - 60
            m += 1
        embed = discord.Embed(title="봇 정보", color=color)
        embed.set_thumbnail(url=ctx.bot.user.avatar.url)
        embed.add_field(name="봇 이름", value=f"{ctx.bot.user.name}")
        embed.add_field(name="현재 버전 해쉬", value=self.bot.githash)
        embed.add_field(
            name="업타임", value=f"{d} 일 {h} 시간 {m} 분 {s} 초"
        )
        embed.add_field(name="봇 ID", value=str(ctx.bot.user.id))
        await ctx.respond(embed=embed)


def setup(bot):
    bot.add_cog(Manage(bot))