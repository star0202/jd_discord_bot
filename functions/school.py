from discord.ext import commands
import discord
from utils.commands import slash_command
from discord.commands import ApplicationContext, Option
import logging
from comcigan import School as GetSchool
from config import COLOR, BAD

logger = logging.getLogger(__name__)
jd = GetSchool("중동중학교")
days = ["월", "화", "수", "목", "금", "토"]


class School(commands.Cog):
    @slash_command(name="시간표", description="오늘 시간표를 출력합니다.")
    async def schedule(
            self,
            ctx: ApplicationContext,
            grade_num: Option(int, name="학년", description="학년을 입력하세요"),
            class_num: Option(int, name="반", description="반을 입력하세요")
    ):
        embed = discord.Embed(title=f"{grade_num}학년 {class_num}반 시간표", color=COLOR)
        try:
            jd[grade_num][class_num]
        except IndexError:
            embed = discord.Embed(title="오류 발생", description="학년, 반을 다시 한번 확인해주세요", color=BAD)
            return await ctx.respond(embed=embed)
        for day in range(6):
            try:
                temp = ""
                for classes in jd[grade_num][class_num][day]:
                    temp += classes[0] + " "
                if temp == "":
                    embed.add_field(name=f"{days[day]}요일", value="정보 없음", inline=False)
                else:
                    embed.add_field(name=f"{days[day]}요일", value=temp, inline=False)
            except IndexError:
                continue
        await ctx.respond(embed=embed)


def setup(bot):
    logger.info("Loaded")
    bot.add_cog(School())


def teardown():
    logger.info("Unloaded")
