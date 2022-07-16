import discord
from discord.ext import commands
from utils.commands import slash_command
from discord.commands import ApplicationContext, Option
from config import COLOR, BAD
from utils.hanspell import spell_checker
import logging

logger = logging.getLogger(__name__)


class SpellCheck(commands.Cog):
    @slash_command(name="맞춤법", description="맞춤법을 검사합니다.")
    async def spellcheck(self, ctx: ApplicationContext, data: Option(str, "검사할 문장을 입력하세요.", name="내용")):
        result = spell_checker.check(data).as_dict()
        if result["errors"] > 0:
            embed = discord.Embed(title="맞춤법 오류 발견", color=BAD)
            embed.add_field(name="발견된 오류 개수", value=result["errors"], inline=False)
            embed.add_field(name="수정된 문장", value=result["checked"], inline=False)
            await ctx.respond(embed=embed)
        else:
            embed = discord.Embed(title="맞춤법 오류 없음", color=COLOR)
            embed.add_field(name="문장", value=result["original"])
            await ctx.respond(embed=embed)


def setup(bot):
    logger.info("Loaded")
    bot.add_cog(SpellCheck())


def teardown():
    logger.info("Unloaded")
