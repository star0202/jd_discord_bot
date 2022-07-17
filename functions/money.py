import discord
import dotenv
from discord.ext import commands
from utils.commands import slash_command
from utils.gettime import get_time
from discord.commands import ApplicationContext, Option
from config import COLOR, BAD
import random
import json
import os
import logging

logger = logging.getLogger(__name__)
dotenv.load_dotenv(".env")


class Money(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @slash_command(name="지원금", description="지원금을 받습니다.")
    async def money_give(self, ctx: ApplicationContext):
        now = get_time()
        db_channel = await self.bot.fetch_channel(os.getenv("DB_CHANNEL_ID"))
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
        given_money *= 5
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
        if ctx.author.id == self.bot.owner_id:
            db_channel = await self.bot.fetch_channel(os.getenv("DB_CHANNEL_ID"))
            db_pins = await db_channel.pins()
            db = db_pins[1]
            await db.edit(jsondata)
            await ctx.respond("Done")

    @slash_command(name="도박", description="지정한 금액이 확률을 통해 사라지거나 2배가 됩니다.")
    async def betting(self, ctx: ApplicationContext, betted_money: Option(int)):
        if betted_money < 100:
            embed = discord.Embed(title="경고", color=BAD, description="최소 베팅 금액은 100원입니다.")
            await ctx.respond(embed=embed)
            return
        if betted_money % 2 != 0:
            embed = discord.Embed(title="경고", color=BAD, description="베팅 금액은 짝수여야 합니다.")
            await ctx.respond(embed=embed)
            return
        db_channel = await self.bot.fetch_channel(os.getenv("DB_CHANNEL_ID"))
        db_pins = await db_channel.pins()
        db = db_pins[1]
        data = json.loads(db.content)
        try:
            if data["users"][str(ctx.author.id)][1] < betted_money:
                embed = discord.Embed(title="경고", color=BAD, description="베팅 금액이 통장 잔액보다 많습니다.")
                await ctx.respond(embed=embed)
                return
        except KeyError:
            embed = discord.Embed(title="경고", color=BAD, description="베팅 금액이 통장 잔액보다 많습니다.")
            await ctx.respond(embed=embed)
            return
        data["users"][str(ctx.author.id)][1] -= betted_money
        bet = random.choice([0, 2])
        data["users"][str(ctx.author.id)][1] += int(betted_money * bet)
        my_money = data["users"][str(ctx.author.id)][1]
        if bet == 0:
            embed = discord.Embed(title="도박 실패", color=BAD, description="도박에 실패하여 베팅 금액이 사라졌습니다..")
            embed.add_field(name="현재 통장", value=f"{my_money}원")
            await ctx.respond(embed=embed)
        else:
            embed = discord.Embed(title="도박 성공", color=COLOR, description="도박에 성공하여 베팅 금액이 2배가 되었습니다!")
            embed.add_field(name="현재 통장", value=f"{my_money}원")
            await ctx.respond(embed=embed)
        await db.edit("\"".join(str(data).split("'")))

    @slash_command(name="통장", description="통장 잔액을 확인합니다.")
    async def money_much(self, ctx: ApplicationContext):
        db_channel = await self.bot.fetch_channel(os.getenv("DB_CHANNEL_ID"))
        db_pins = await db_channel.pins()
        db = db_pins[1]
        data = json.loads(db.content)
        money = data["users"][str(ctx.author.id)][1]
        embed = discord.Embed(title="통장 잔액", color=COLOR, description=f"{money}원")
        await ctx.respond(embed=embed)


def setup(bot):
    logger.info("Loaded")
    bot.add_cog(Money(bot))


def teardown():
    logger.info("Unloaded")
