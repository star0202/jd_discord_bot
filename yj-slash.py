#-*- coding: utf-8 -*-
import discord
from discord.ext import commands
from discord_slash import SlashCommand
from discord_slash.utils.manage_commands import create_option
import asyncio
import math
import time
from config import token

color = 0x2F3136
bad = 0x2F3136
good = 0x2F3136
muted = []
start = time.time()
bot = commands.Bot(command_prefix="f<")
slash = SlashCommand(bot, sync_commands=True, override_type=True)

@bot.event
async def on_ready():
    print("Ready!")
    devdm = await bot.fetch_user(798690702635827200)
    await devdm.send(f"yj-slash.py 실행. <t:{math.trunc(time.time())}:T>")

guild_ids = [842728992103989259]

@slash.slash(name="ping", guild_ids=guild_ids, description="봇의 핑을 알려줍니다")
async def _ping(ctx):
    pingembed = discord.Embed(colour=color)
    pingembed.add_field(name=":ping_pong: 퐁!", value="`" + str(round(round(bot.latency, 4) * 1000)) + "ms`", inline=False)
    await ctx.send(embed=pingembed)

@slash.slash(name="kick", guild_ids=guild_ids,
                description="멤버를 킥합니다",
                options=[
                    create_option(name="user",option_type=6,description="킥할 유저를 입력하세요",required=True),
                    create_option(name="reason",option_type=3,description="추방된 이유를 입력하세요",required=False),
                ])
async def _kick(ctx, user, *, reason="알 수 없음"):
    if ctx.author.guild_permissions.administrator:
        dm = await bot.fetch_user(user.id)
        em = discord.Embed(title="추방되었습니다", description=f"서버: {ctx.guild.name}\n이유: `{reason}`", colour=color)
        await dm.send(embed=em)
        await user.kick()
        em = discord.Embed(title="유저 추방", description=f"유저: {user.mention}\n이유: `{reason}`", colour=color)
        await ctx.send(embed=em)

@slash.slash(name="ban", guild_ids=guild_ids,
                description="멤버를 밴합니다",
                options=[
                    create_option(name="user",option_type=6,description="밴할 유저를 입력하세요",required=True),
                    create_option(name="reason",option_type=3,description="차단된 이유를 입력하세요",required=False),
                ])
async def _ban(ctx, user, *, reason="알 수 없음"):
    if ctx.author.guild_permissions.administrator:
        dm = await bot.fetch_user(user.id)
        em = discord.Embed(title="차단되었습니다", description=f"서버: {ctx.guild.name}\n이유: `{reason}`", colour=color)
        await dm.send(embed=em)
        await user.ban()
        em = discord.Embed(title="유저 차단", description=f"유저: {user.mention}\n이유: `{reason}`", colour=color)
        await ctx.send(embed=em)

@slash.slash(name="warn", guild_ids=guild_ids,
                description="멤버를 경고합니다",
                options=[
                    create_option(name="user",option_type=6,description="경고할 유저를 입력하세요",required=True),
                    create_option(name="reason",option_type=3,description="경고한 이유를 입력하세요",required=False),
                ])
async def _warn(ctx, user, *, reason="알 수 없음"):
    if ctx.author.guild_permissions.administrator:
        await user.remove_roles(bot.get_guild(842728992103989259).get_role(859237801898803210))
        if "__경고 1__" in str(user.roles):
            await user.remove_roles(bot.get_guild(842728992103989259).get_role(864291233040171019))
            await user.add_roles(bot.get_guild(842728992103989259).get_role(864291299518709811), reason = reason)
            dm = await bot.fetch_user(user.id)
            em = discord.Embed(title="경고 2회", description=f"서버: {ctx.guild.name}\n이유: `{reason}`", colour=bad)
            await dm.send(embed=em)
            em = discord.Embed(title="경고 2회", description=f"유저: {user.mention}\n이유: `{reason}`", colour=bad)
            await ctx.send(embed=em)
        elif "__경고 2__" in str(user.roles):
            await user.remove_roles(bot.get_guild(842728992103989259).get_role(864291299518709811))
            await user.add_roles(bot.get_guild(842728992103989259).get_role(864291333023072256), reason = reason)
            dm = await bot.fetch_user(user.id)
            em = discord.Embed(title="경고 3회", description=f"서버: {ctx.guild.name}\n이유: `{reason}`", colour=bad)
            await dm.send(embed=em)
            em = discord.Embed(title="경고 3회", description=f"유저: {user.mention}\n이유: `{reason}`", colour=bad)
            await ctx.send(embed=em)
        elif "__경고 3__" in str(user.roles):
            await user.remove_roles(bot.get_guild(842728992103989259).get_role(864291333023072256))
            dm = await bot.fetch_user(user.id)
            em = discord.Embed(title="경고 누적으로 추방", description=f"서버: {ctx.guild.name}", colour=bad)
            await dm.send(embed=em)
            em = discord.Embed(title="경고 누적으로 추방", description=f"유저: {user.mention}\n이유: `{reason}`", colour=bad)
            await ctx.send(embed=em)
            await user.kick()
        else:
            await user.add_roles(bot.get_guild(842728992103989259).get_role(864291233040171019), reason=reason)
            dm = await bot.fetch_user(user.id)
            em=discord.Embed(title="경고 1회", description=f"서버: {ctx.guild.name}\n이유: `{reason}`",colour=bad)
            await dm.send(embed=em)
            em = discord.Embed(title="경고 1회", description=f"유저: {user.mention}\n이유: `{reason}`", colour=bad)
            await ctx.send(embed=em)

@slash.slash(name="unwarn", guild_ids=guild_ids,
                description="멤버의 경고를 해제합니다",
                options=[
                    create_option(name="user",option_type=6,description="경고를 해제할 유저를 입력하세요",required=True)
                ])
async def _unwarn(ctx, user: discord.Member):
    if ctx.author.guild_permissions.administrator:
        await user.add_roles(bot.get_guild(842728992103989259).get_role(859237801898803210))
        if "__경고 1__" in str(user.roles):
            dm = await bot.fetch_user(user.id)
            await user.remove_roles(bot.get_guild(842728992103989259).get_role(864291233040171019))
        elif "__경고 2__" in str(user.roles):
            dm = await bot.fetch_user(user.id)
            await user.remove_roles(bot.get_guild(842728992103989259).get_role(864291299518709811))
        elif "__경고 3__" in str(user.roles):
            dm = await bot.fetch_user(user.id)
            await user.remove_roles(bot.get_guild(842728992103989259).get_role(864291333023072256))
        em = discord.Embed(title="경고 제거", description=f"서버: {ctx.guild.name}", colour=good)
        await dm.send(embed=em)
        em = discord.Embed(title="경고 제거", description=f"유저: {user.mention}", colour=good)
        await ctx.send(embed=em)

@slash.slash(name="mute", guild_ids=guild_ids,
                description="멤버를 뮤트합니다",
                options=[
                    create_option(name="user",option_type=6,description="뮤트할 유저를 입력하세요",required=True),
                    create_option(name="time",option_type=3,description="뮤트할 시간을 입력하세요",required=False)
                ])
async def _mute(ctx, user: discord.Member, *, time="infinity"):
    if ctx.author.guild_permissions.administrator:
        await user.remove_roles(bot.get_guild(842728992103989259).get_role(859237801898803210))
        if time[len(time)-1] == "s":
            realtime = int(time[0:len(time) - 1])
            infotime = time[0:len(time) - 1] + "초"
        elif time[len(time)-1] == "m":
            realtime = 60 * int(time[0:len(time) - 1])
            infotime = time[0:len(time) - 1] + "분"
        elif time == "infinity":
            infotime = "언뮤트 될 때 까지"
            await user.add_roles(bot.get_guild(842728992103989259).get_role(857583384606801960))
            muted.append(user.id)
            dm = await bot.fetch_user(user.id)
            em = discord.Embed(title="뮤트되었습니다", description=f"서버: {ctx.guild.name}\n시간: `{infotime}`", colour=bad)
            await dm.send(embed=em)
            em = discord.Embed(title="뮤트", description=f"유저: {user.mention}\n시간: `{infotime}`", colour=bad)
            await ctx.send(embed=em)
            return
        await user.add_roles(bot.get_guild(842728992103989259).get_role(857583384606801960))
        muted.append(user.id)
        dm = await bot.fetch_user(user.id)
        em = discord.Embed(title="뮤트되었습니다", description=f"서버: {ctx.guild.name}\n시간: `{infotime}`", colour=bad)
        await dm.send(embed=em)
        em = discord.Embed(title="뮤트", description=f"유저: {user.mention}\n시간: `{infotime}`", colour=bad)
        await ctx.send(embed=em)
        await asyncio.sleep(realtime)
        if user.id in muted:
            await user.add_roles(bot.get_guild(842728992103989259).get_role(859237801898803210))
            await user.remove_roles(bot.get_guild(842728992103989259).get_role(857583384606801960))
            em = discord.Embed(title="뮤트가 해제되었습니다", description=f"서버: {ctx.guild.name}", colour=good)
            await dm.send(embed=em)
            em = discord.Embed(title="뮤트 해제", description=f"유저: {user.mention}", colour=good)
            await ctx.send(embed=em)
            muted.remove(user.id)

@slash.slash(name="unmute", guild_ids=guild_ids,
                description="멤버를 언뮤트합니다",
                options=[
                    create_option(name="user",option_type=6,description="언뮤트할 유저를 입력하세요",required=True)
                ])
async def _unmute(ctx, user: discord.Member):
    if ctx.author.guild_permissions.administrator:
        await user.add_roles(bot.get_guild(842728992103989259).get_role(859237801898803210))
        await user.remove_roles(bot.get_guild(842728992103989259).get_role(857583384606801960))
        dm = await bot.fetch_user(user.id)
        em = discord.Embed(title="뮤트가 해제되었습니다", description=f"서버: {ctx.guild.name}", colour=good)
        await dm.send(embed=em)
        em = discord.Embed(title="뮤트 해제", description=f"유저: {user.mention}", colour=good)
        await ctx.send(embed=em)
        muted.remove(user.id)

@slash.slash(name="eval", guild_ids=guild_ids,
                description="코드를 실행합니다",
                options=[
                    create_option(name="code",option_type=3,description="실행할 코드를 입력하세요",required=True)
                ])
async def _eval(ctx, code):
    evalembed = discord.Embed(colour=color, title="Eval")
    evalembed.add_field(name="Input", value="```python\n" + code + "```", inline=False)
    try:
        evalembed.add_field(name="Output", value="```" + str(eval(code)) + "```")
        await ctx.send(embed=evalembed)
    except Exception as ex:
        evalembed.add_field(name="Output", value="```python\n" + str(ex) + "```")
        await ctx.send(embed=evalembed)

@slash.slash(name="정보", guild_ids=guild_ids, description="봇의 정보를 알려줍니다")
async def _info(ctx):
    infotime = time.time()
    S = round(infotime - start)
    D = 0
    H = 0
    M = 0
    while S >= 86400:
        S = S - 86400
        D += 1
    while S >= 3600:
        S = S - 3600
        H += 1
    while S >= 60:
        S = S - 60
        M += 1
    infoembed = discord.Embed(title=bot.user.name, colour=color)
    infoembed.add_field(name="업타임", value="{0} 일 {1} 시간 {2} 분 {3} 초".format(D, H, M, S), inline=True)
    infoembed.add_field(name="아이디", value=bot.user.id, inline=True)
    infoembed.add_field(name=":technologist: 개발자:technologist: ", value="<@!798690702635827200>", inline=True)
    infoembed.set_footer(text="Made with discord.py", icon_url="https://i.imgur.com/8ciREEh.jpg")
    await ctx.send(embed=infoembed)

bot.run(token)