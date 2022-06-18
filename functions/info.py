from discord.ext import commands
import discord
from utils.commands import slash_command
from utils.timeconvert import datetime_to_unix
from discord.commands import ApplicationContext, Option
from config import color


class Info(commands.Cog):
    @slash_command(name="유저정보", description="유저의 정보를 출력합니다.")
    async def userinfo(
        self,
        ctx: ApplicationContext,
        user: Option(
            discord.Member, required=False, name="유저", description="정보를 출력할 유저를 입력하세요, 자신을 원한다면 비워두세요."
        )
    ):
        if user is None:
            user = ctx.author
        if user.color == discord.Colour.default():
            embed = discord.Embed(colour=color, title=user.display_name)
        else:
            embed = discord.Embed(colour=user.color, title=user.display_name)
        embed.set_thumbnail(url=user.display_avatar.url)
        embed.add_field(name="계정명", value=user.name + "#" + user.discriminator)
        embed.add_field(name="닉네임", value=user.display_name)
        embed.add_field(name="ID", value=str(user.id))
        embed.add_field(name="최상위 역할", value=str(user.top_role))
        embed.add_field(name="계정 생성 날짜", value=f"<t:{datetime_to_unix(user.created_at)}:R> ({user.created_at})")
        await ctx.respond(embed=embed)


def setup(bot):
    bot.add_cog(Info())
