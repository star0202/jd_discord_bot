import discord
from discord.ext import commands
from utils.commands import slash_command
from discord.commands import ApplicationContext, Option
from config import color, bad
import time
import asyncio


class Manage(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @slash_command(name="핑", description="봇의 핑을 전송합니다.")
    async def ping(self, ctx: ApplicationContext):
        embed = discord.Embed(title=":ping_pong: 퐁!", color=color)
        embed.add_field(
            name="discord API Ping: ", value=f"{round(ctx.bot.latency * 1000)} ms"
        )
        await ctx.respond(embed=embed)

    @slash_command(name="봇", description="봇의 정보를 전송합니다.")
    async def botinfo(self, ctx: ApplicationContext):
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
        embed.add_field(name="봇 이름", value=f"**{ctx.bot.user.name}** ({str(ctx.bot.user)})", inline=False)
        embed.add_field(
            name="업타임", value=f"{d} 일 {h} 시간 {m} 분 {s} 초",
            inline=False
        )
        embed.add_field(name="봇 ID", value=str(ctx.bot.user.id), inline=False)
        await ctx.respond(embed=embed)

    @slash_command(name="청소", description="메시지를 일정 개수만큼 지웁니다.")
    async def clear(
        self, ctx: ApplicationContext, count: Option(int, "삭제할 메시지의 개수를 입력하세요.")
    ):
        if ctx.author.guild_permissions.administrator:
            if count:
                await ctx.channel.purge(limit=count)
                embed = discord.Embed(title="청소 완료!", color=color)
                embed.add_field(name="삭제한 메시지의 수:", value=f"{count}", inline=False)
                await ctx.respond(embed=embed)
            else:
                embed = discord.Embed(title="오류 발생!", color=bad)
                embed.add_field(name="값 오류", value="올바른 자연수 값을 입력해주세요.")
        else:
            embed = discord.Embed(title="오류 발생!", color=bad)
            embed.add_field(name="권한 오류", value="권한 확인 후 다시 시도해주세요.", inline=False)
            await ctx.respond(embed=embed)


def setup(bot):
    bot.add_cog(Manage(bot))
