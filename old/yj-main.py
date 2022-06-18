# -*- coding: utf-8 -*-
from discord.ext import commands
import discord
import requests
from bs4 import BeautifulSoup
import random
import datetime
import time
import infomaker
from googletrans import Translator
import math
from config import token

bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())
bot.remove_command("help")
translator = Translator()
muted = []
color = 0x2F3136
bad = 0x2F3136
good = 0x2F3136
timer = {}
_info = infomaker.maker()
start = time.time()
badwords = ["씨발", "시발", "병신", "섹스", "꺼져", "새끼", "닥쳐", "자위", "좆", "담배"]


@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------------')
    devdm = await bot.fetch_user(798690702635827200)
    await devdm.send(f"yj-main.py 실행. <t:{math.trunc(time.time())}:T>")
    await bot.change_presence(activity=discord.Game(name="!도움 으로 명령어를 확인하세요"))


@bot.command(name="핑")
async def ping(ctx):
    pingembed = discord.Embed(colour=color)
    pingembed.add_field(name=":ping_pong: 퐁!", value="`" + str(round(round(bot.latency, 4) * 1000)) + "ms`",
                        inline=False)
    await ctx.send(embed=pingembed)


@bot.command()
@commands.has_permissions(kick_members=True)
async def k(ctx, member: discord.Member, *, reason="알 수 없음"):
    dm = await bot.fetch_user(member.id)
    em = discord.Embed(title="추방되었습니다", description=f"서버: {ctx.guild.name}\n이유: `{reason}`", colour=bad)
    try:
        await dm.send(embed=em)
    except:
        pass
    await member.kick()
    em = discord.Embed(title="유저 추방", description=f"유저: {member.mention}\n이유: `{reason}`", colour=bad)
    await ctx.send(embed=em)


@bot.command()
@commands.has_permissions(ban_members=True)
async def b(ctx, member: discord.Member, *, reason="알 수 없음"):
    dm = await bot.fetch_user(member.id)
    em = discord.Embed(title="차단되었습니다", description=f"서버: {ctx.guild.name}\n이유: `{reason}`", colour=bad)
    try:
        await dm.send(embed=em)
    except:
        pass
    await member.ban()
    em = discord.Embed(title="유저 차단", description=f"유저: {member.mention}\n이유: `{reason}`", colour=bad)
    await ctx.send(embed=em)


@bot.command()
async def kill(ctx):
    if int(ctx.message.author.id) == 798690702635827200:
        em = discord.Embed(title="봇이 종료됩니다", colour=color)
        await ctx.send(embed=em)
        try:
            await bot.close()
        except:
            print("EnvironmentError")
            bot.clear()


@bot.command(name="eval")
async def evalcommand(ctx, *, content: str):
    evalembed = discord.Embed(colour=color, title="Eval")
    evalembed.add_field(name="Input", value="```python\n" + content + "```", inline=False)
    try:
        evalembed.add_field(name="Output", value="```python\n" + str(eval(content)) + "```")
        await ctx.send(embed=evalembed)
    except Exception as ex:
        evalembed.add_field(name="Output", value="```python\n" + str(ex) + "```")
        await ctx.send(embed=evalembed)


@bot.command(name="주사위")
async def dice(ctx):
    dicel = random.choice([":one:이", ":two:가", ":three:이", ":four:가", ":five:가", ":six:이"])  # 뒤 글자도 써야함
    await ctx.send("데구르르... " + dicel + " 나왔어요!")


@bot.command(name="날짜")
async def date(ctx):
    nowtime = datetime.date.today()
    await ctx.send(nowtime.strftime("20%y년 %m월 %d일 입니다."))


async def info(ctx):
    infotime = float(time.time())
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
    infoembed.add_field(name="아이디", value=str(bot.user.id), inline=True)
    infoembed.add_field(name=":technologist: 개발자:technologist: ", value="<@!798690702635827200>", inline=True)
    infoembed.set_footer(text="Made with discord.py", icon_url="https://i.imgur.com/8ciREEh.jpg")
    await ctx.send(embed=infoembed)


@bot.command(name="유저정보")
async def usrinfo(ctx, member: discord.Member = None):
    if member == None:
        member = ctx.author
    if member.color == discord.Colour.default():
        userembed = discord.Embed(colour=color, title=member.display_name)
    else:
        userembed = discord.Embed(colour=member.color, title=member.display_name)
    userembed.set_thumbnail(url=member.display_avatar.url)
    userembed.add_field(name="계정명", value=member.name + "#" + member.discriminator)
    userembed.add_field(name="닉네임", value=member.display_name)
    userembed.add_field(name="ID", value=str(member.id))
    userembed.add_field(name="최상위 역할", value=str(member.top_role))
    userembed.add_field(name="계정 생성 날짜", value=str(member.created_at))
    await ctx.send(embed=userembed)


@bot.command(name="고양이")
async def cat(ctx):
    html = requests.get("https://some-random-api.ml/img/cat")
    soup = BeautifulSoup(html.text)
    catembed = discord.Embed(colour=color)
    catembed.set_image(url=str(soup)[str(soup).find("https://"):str(soup).find("\"}")])
    catembed.set_footer(text="Powered by some-random-api.ml", icon_url="https://i.some-random-api.ml/logo.png")
    await ctx.send(embed=catembed)


@bot.command(name="강아지")
async def dog(ctx):
    html = requests.get("https://some-random-api.ml/img/dog")
    soup = BeautifulSoup(html.text)
    dogembed = discord.Embed(colour=color)
    dogembed.set_image(url=str(soup)[str(soup).find("https://"):str(soup).find("\"}")])
    dogembed.set_footer(text="Powered by some-random-api.ml", icon_url="https://i.some-random-api.ml/logo.png")
    await ctx.send(embed=dogembed)


@bot.command(name="급식")
async def food(ctx):
    em = discord.Embed(title="급식", description=_info.school_menu("양전초등학교"), colour=color)
    await ctx.send(embed=em)


@bot.command(name="날씨")
async def weather(ctx, *, content):
    Finallocation = content + '날씨'
    CheckDust = []
    url = 'https://search.naver.com/search.naver?where=nexearch&sm=top_hty&fbm=1&ie=utf8&query=' + Finallocation
    hdr = {'User-Agent': (
        'mozilla/5.0 (windows nt 10.0; win64; x64) applewebkit/537.36 (khtml, like gecko) chrome/78.0.3904.70 safari/537.36')}
    req = requests.get(url, headers=hdr)
    html = req.text
    soup = BeautifulSoup(html, 'html.parser')
    ErrorCheck = soup.find('span', {'class': 'btn_select'})
    if 'None' in str(ErrorCheck):
        await ctx.send("**[ERROR]**지역을 찾을 수 없습니다, 지역 이름을 간단히, 혹은 자세히 써주세요.")
        return
    for i in soup.select('span[class=btn_select]'):
        LocationInfo = i.text
        NowTemp = soup.find('span', {'class': 'todaytemp'}).text + soup.find('span', {'class': 'tempmark'}).text[2:]
        WeatherCast = soup.find('p', {'class': 'cast_txt'}).text
        TodayMorningTemp = soup.find('span', {'class': 'min'}).text
        TodayAfternoonTemp = soup.find('span', {'class': 'max'}).text
        TodayFeelTemp = soup.find('span', {'class': 'sensible'}).text[5:]
        CheckDust1 = soup.find('div', {'class': 'sub_info'})
        CheckDust2 = CheckDust1.find('div', {'class': 'detail_box'})
        for x in CheckDust2.select('dd'):
            CheckDust.append(x.text)
        FineDust = CheckDust[0][:-2] + " " + CheckDust[0][-2:]
        UltraFineDust = CheckDust[1][:-2] + " " + CheckDust[1][-2:]
        Ozon = CheckDust[2][:-2] + " " + CheckDust[2][-2:]
        tomorrowArea = soup.find('div', {'class': 'tomorrow_area'})
        tomorrowCheck = tomorrowArea.find_all('div', {'class': 'main_info morning_box'})
        tomorrowMoring1 = tomorrowCheck[0].find('span', {'class': 'todaytemp'}).text
        tomorrowMoring2 = tomorrowCheck[0].find('span', {'class': 'tempmark'}).text[2:]
        tomorrowMoring = tomorrowMoring1 + tomorrowMoring2
        tomorrowMState1 = tomorrowCheck[0].find('div', {'class': 'info_data'})
        tomorrowMState2 = tomorrowMState1.find('ul', {'class': 'info_list'})
        tomorrowMState3 = tomorrowMState2.find('p', {'class': 'cast_txt'}).text
        tomorrowMState4 = tomorrowMState2.find('div', {'class': 'detail_box'})
        tomorrowMState5 = tomorrowMState4.find('span').text.strip()
        tomorrowMState = tomorrowMState3 + " " + tomorrowMState5
        tomorrowAfter1 = tomorrowCheck[1].find('p', {'class': 'info_temperature'})
        tomorrowAfter2 = tomorrowAfter1.find('span', {'class': 'todaytemp'}).text
        tomorrowAfter3 = tomorrowAfter1.find('span', {'class': 'tempmark'}).text[2:]
        tomorrowAfter = tomorrowAfter2 + tomorrowAfter3
        tomorrowAState1 = tomorrowCheck[1].find('div', {'class': 'info_data'})
        tomorrowAState2 = tomorrowAState1.find('ul', {'class': 'info_list'})
        tomorrowAState3 = tomorrowAState2.find('p', {'class': 'cast_txt'}).text
        tomorrowAState4 = tomorrowAState2.find('div', {'class': 'detail_box'})
        tomorrowAState5 = tomorrowAState4.find('span').text.strip()
        tomorrowAState = tomorrowAState3 + " " + tomorrowAState5
        embed = discord.Embed(title=LocationInfo + " 날씨 정보", colour=color)
        embed.add_field(name="오늘 날씨",
                        value=":thermometer: 현재온도: " + NowTemp + "\n" + ":thermometer: 체감온도: " + TodayFeelTemp + "\n" \
                              + ":thermometer: 오전/오후 온도: " + TodayMorningTemp + "/" + TodayAfternoonTemp + "\n" + "현재 상태: " + WeatherCast + "\n" \
                              + "현재 미세먼지 농도: " + FineDust + "\n" \
                              + "현재 초미세먼지 농도: " + UltraFineDust + "\n" + "현재 오존 지수: " + Ozon, inline=False)
        embed.add_field(name="내일 날씨", value=":thermometer: 내일 오전 온도: " + tomorrowMoring + "\n" \
                                            + "내일 오전 상태: " + tomorrowMState + "\n" + ":thermometer: 내일 오후 온도: " + tomorrowAfter + "\n" \
                                            + "내일 오후 상태: " + tomorrowAState, inline=False)
        embed.set_footer(text="Powered by naver.com",
                         icon_url="https://www.gnewsbiz.com/news/photo/202006/22508_23046_17.png")
        await ctx.send(embed=embed)


@bot.command(name="번역")
async def trans(ctx, inputlang, outputlang, *, content):
    await ctx.send(content)
    result = translator.translate(str(content), src=inputlang, dest=outputlang)
    em = discord.Embed(title="번역", colour=color)
    em.add_field(name=f"Input({inputlang})", value=f"```\n{content}```")
    em.add_field(name=f"Output({outputlang})", value=f"```\n{result.text}```")
    em.set_footer(text="Powered by Google",
                  icon_url="https://upload.wikimedia.org/wikipedia/commons/thumb/5/53/Google_%22G%22_Logo.svg/1200px-Google_%22G%22_Logo.svg.png")
    await ctx.send(embed=em)


@bot.command(name="건의")
async def dmtodev(ctx, *, content: str):
    embed = discord.Embed(colour=color, title="건의")
    embed.add_field(name="건의자", value=f"{ctx.author.name}#{ctx.author.discriminator}({ctx.author.id})", inline=False)
    embed.add_field(name="내용", value=content, inline=False)
    devdm = await bot.fetch_user(798690702635827200)
    await devdm.send(embed=embed)


@bot.event
async def on_message(message):
    msgcontent = message.content
    bad = 0
    for x in range(0, len(badwords)):
        bad = bad + msgcontent.find(badwords[x]) + 1
    if bad != 0:
        badembed = discord.Embed(title=":no_entry_sign:욕설/금지어 사용 경고:no_entry_sign:",
                                 description=str(message.author.mention) \
                                             + "님이 욕설/금지어를 사용하셨습니다.", colour=color)
        await message.delete()
        await message.channel.send(embed=badembed)
    await bot.process_commands(message)


bot.run(token)
