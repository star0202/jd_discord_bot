from discord.ext import commands
import logging
from discord import ApplicationContext
from utils.commands import slash_command
import requests
from bs4 import BeautifulSoup
import discord
from config import COLOR, COVID_SELECTORS

logger = logging.getLogger(__name__)


class Covid(commands.Cog):
    @slash_command(name="코로나", description="코로나 관련 정보를 출력합니다.")
    async def get_covid(self, ctx: ApplicationContext):
        response = requests.get("http://ncov.mohw.go.kr/")
        html = response.text
        soup = BeautifulSoup(html, 'html.parser')
        death = soup.select_one(COVID_SELECTORS["death"]).get_text()
        confirmed = soup.select_one(COVID_SELECTORS["confirmed"]).get_text()
        total_death = soup.select_one(COVID_SELECTORS["total_death"]).get_text()[6:]
        total_confirmed = soup.select_one(COVID_SELECTORS["total_confirmed"]).get_text()[6:-4]
        embed = discord.Embed(title="코로나 현황", color=COLOR)
        embed.add_field(name="오늘 사망자", value=f"{death}명")
        embed.add_field(name="오늘 확진자", value=f"{confirmed}명")
        embed.add_field(name="누적 사망자", value=f"{total_death}명")
        embed.add_field(name="누적 확진자", value=f"{total_confirmed}명")
        await ctx.respond(embed=embed)


def setup(bot):
    logger.info("Loaded")
    bot.add_cog(Covid())


def teardown():
    logger.info("Unloaded")
