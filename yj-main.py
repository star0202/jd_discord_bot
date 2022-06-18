#-*- coding: utf-8 -*-
from discord.ext import commands
from discordTogether import DiscordTogether
import discord
import asyncio
import youtube_dl
import requests
from bs4 import BeautifulSoup
import random
import datetime
import time
import infomaker
import googletrans
import math
from config import token

bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())
bot.remove_command("help")
togetherControl = DiscordTogether(bot)
translator = googletrans.Translator()
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

@bot.command(name = "핑")
async def ping(ctx):
    pingembed = discord.Embed(colour=color)
    pingembed.add_field(name=":ping_pong: 퐁!", value="`" + str(round(round(bot.latency, 4) * 1000)) + "ms`", inline=False)
    await ctx.send(embed=pingembed)

@bot.command()
@commands.has_permissions(administrator=True)
async def w(ctx, member: discord.Member, *, reason="알 수 없음"):
    await member.remove_roles(bot.get_guild(842728992103989259).get_role(859237801898803210))
    if "__경고 1__" in str(member.roles):
        await member.remove_roles(bot.get_guild(842728992103989259).get_role(864291233040171019))
        await member.add_roles(bot.get_guild(842728992103989259).get_role(864291299518709811), reason = reason)
        dm = await bot.fetch_user(member.id)
        em = discord.Embed(title="경고 2회", description=f"서버: {ctx.guild.name}\n이유: `{reason}`", colour=bad)
        await dm.send(embed=em)
        em = discord.Embed(title="경고 2회", description=f"유저: {member.mention}\n이유: `{reason}`", colour=bad)
        await ctx.send(embed=em)
    elif "__경고 2__" in str(member.roles):
        await member.remove_roles(bot.get_guild(842728992103989259).get_role(864291299518709811))
        await member.add_roles(bot.get_guild(842728992103989259).get_role(864291333023072256), reason = reason)
        dm = await bot.fetch_user(member.id)
        em = discord.Embed(title="경고 3회", description=f"서버: {ctx.guild.name}\n이유: `{reason}`", colour=bad)
        await dm.send(embed=em)
        em = discord.Embed(title="경고 3회", description=f"유저: {member.mention}\n이유: `{reason}`", colour=bad)
        await ctx.send(embed=em)
    elif "__경고 3__" in str(member.roles):
        await member.remove_roles(bot.get_guild(842728992103989259).get_role(864291333023072256))
        dm = await bot.fetch_user(member.id)
        em = discord.Embed(title="경고 누적으로 추방", description=f"서버: {ctx.guild.name}", colour=bad)
        await dm.send(embed=em)
        em = discord.Embed(title="경고 누적으로 추방", description=f"유저: {member.mention}\n이유: `{reason}`", colour=bad)
        await ctx.send(embed=em)
        await member.kick()
    else:
        await member.add_roles(bot.get_guild(842728992103989259).get_role(864291233040171019), reason=reason)
        dm = await bot.fetch_user(member.id)
        em=discord.Embed(title="경고 1회", description=f"서버: {ctx.guild.name}\n이유: `{reason}`",colour=bad)
        await dm.send(embed=em)
        em = discord.Embed(title="경고 1회", description=f"유저: {member.mention}\n이유: `{reason}`", colour=bad)
        await ctx.send(embed=em)

@bot.command()
@commands.has_permissions(administrator=True)
async def k(ctx, member: discord.Member, *, reason="알 수 없음"):
    dm = await bot.fetch_user(member.id)
    em = discord.Embed(title="추방되었습니다", description=f"서버: {ctx.guild.name}\n이유: `{reason}`", colour=bad)
    await dm.send(embed=em)
    await member.kick()
    em = discord.Embed(title="유저 추방", description=f"유저: {member.mention}\n이유: `{reason}`", colour=bad)
    await ctx.send(embed=em)

@bot.command()
@commands.has_permissions(administrator=True)
async def b(ctx, member: discord.Member, *, reason="알 수 없음"):
    dm = await bot.fetch_user(member.id)
    em = discord.Embed(title="차단되었습니다", description=f"서버: {ctx.guild.name}\n이유: `{reason}`", colour=bad)
    await dm.send(embed=em)
    await member.ban()
    em = discord.Embed(title="유저 차단", description=f"유저: {member.mention}\n이유: `{reason}`", colour=bad)
    await ctx.send(embed=em)

@bot.command()
@commands.has_permissions(administrator=True)
async def uw(ctx, member: discord.Member):
    await member.add_roles(bot.get_guild(842728992103989259).get_role(859237801898803210))
    if "__경고 1__" in str(member.roles):
        dm = await bot.fetch_user(member.id)
        await member.remove_roles(bot.get_guild(842728992103989259).get_role(864291233040171019))
    elif "__경고 2__" in str(member.roles):
        dm = await bot.fetch_user(member.id)
        await member.remove_roles(bot.get_guild(842728992103989259).get_role(864291299518709811))
    elif "__경고 3__" in str(member.roles):
        dm = await bot.fetch_user(member.id)
        await member.remove_roles(bot.get_guild(842728992103989259).get_role(864291333023072256))
    em = discord.Embed(title="경고 제거", description=f"서버: {ctx.guild.name}", colour=good)
    await dm.send(embed=em)
    em = discord.Embed(title="경고 제거", description=f"유저: {member.mention}", colour=good)
    await ctx.send(embed=em)

@bot.command()
@commands.has_permissions(administrator=True)
async def m(ctx, member: discord.Member, *, time="infinity"):
    await member.remove_roles(bot.get_guild(842728992103989259).get_role(859237801898803210))
    if time[len(time)-1] == "s":
        realtime = int(time[0:len(time) - 1])
        infotime = time[0:len(time) - 1] + "초"
    elif time[len(time)-1] == "m":
        realtime = 60 * int(time[0:len(time) - 1])
        infotime = time[0:len(time) - 1] + "분"
    elif time == "infinity":
        infotime = "언뮤트 될 때 까지"
        await member.add_roles(bot.get_guild(842728992103989259).get_role(857583384606801960))
        muted.append(member.id)
        dm = await bot.fetch_user(member.id)
        em = discord.Embed(title="뮤트되었습니다", description=f"서버: {ctx.guild.name}\n시간: `{infotime}`", colour=bad)
        await dm.send(embed=em)
        em = discord.Embed(title="뮤트", description=f"유저: {member.mention}\n시간: `{infotime}`", colour=bad)
        await ctx.send(embed=em)
        return
    await member.add_roles(bot.get_guild(842728992103989259).get_role(857583384606801960))
    muted.append(member.id)
    dm = await bot.fetch_user(member.id)
    em = discord.Embed(title="뮤트되었습니다", description=f"서버: {ctx.guild.name}\n시간: `{infotime}`", colour=bad)
    await dm.send(embed=em)
    em = discord.Embed(title="뮤트", description=f"유저: {member.mention}\n시간: `{infotime}`", colour=bad)
    await ctx.send(embed=em)
    await asyncio.sleep(realtime)
    if member.id in muted:
        await member.add_roles(bot.get_guild(842728992103989259).get_role(859237801898803210))
        await member.remove_roles(bot.get_guild(842728992103989259).get_role(857583384606801960))
        em = discord.Embed(title="뮤트가 해제되었습니다", description=f"서버: {ctx.guild.name}", colour=good)
        await dm.send(embed=em)
        em = discord.Embed(title="뮤트 해제", description=f"유저: {member.mention}", colour=good)
        await ctx.send(embed=em)
        muted.remove(member.id)

@bot.command()
@commands.has_permissions(administrator=True)
async def um(ctx, member: discord.Member):
    await member.add_roles(bot.get_guild(842728992103989259).get_role(859237801898803210))
    await member.remove_roles(bot.get_guild(842728992103989259).get_role(857583384606801960))
    dm = await bot.fetch_user(member.id)
    em = discord.Embed(title="뮤트가 해제되었습니다", description=f"서버: {ctx.guild.name}", colour=good)
    await dm.send(embed=em)
    em = discord.Embed(title="뮤트 해제", description=f"유저: {member.mention}", colour=good)
    await ctx.send(embed=em)
    muted.remove(member.id)

@bot.command()
async def kill(ctx):
    if int(ctx.message.author.id) == 798690702635827200:
        em = discord.Embed(title="봇이 종료됩니다", colour=color)
        await ctx.send(embed=em)
        try:
            await bot.logout()
        except:
            print("EnvironmentError")
            bot.clear()

@bot.command(name = "eval")
async def evalcommand(ctx, *, content: str):
    evalembed = discord.Embed(colour=color, title="Eval")
    evalembed.add_field(name="Input", value="```python\n" + content + "```", inline=False)
    try:
        evalembed.add_field(name="Output", value="```python\n" + str(eval(content)) + "```")
        await ctx.send(embed=evalembed)
    except Exception as ex:
        evalembed.add_field(name="Output", value="```python\n" + str(ex) + "```")
        await ctx.send(embed=evalembed)

@bot.command(name="재생", aliases=["play", "p"])
async def play(ctx, url, soundvolume=0.7):
    channel = ctx.author.voice.channel
    if channel is None:
        em = discord.Embed(title="오류", description="음성채널에 들어가 주세요", colour=bad)
        await ctx.send(embed=em)
        return
    if bot.voice_clients == []:
        await channel.connect()
        html = requests.get(url)
        soup = BeautifulSoup(html.text, "html.parser")
        title = str(soup)[str(soup).find("<title>")+7:str(soup).find("</title>")-10]
        em = discord.Embed(title="재생 시작", description=f"제목: {title}", colour=color)
        await ctx.send(embed=em)
        ydl_opts = {'format': 'bestaudio'}
        FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            URL = info['formats'][0]['url']
        voice = bot.voice_clients[0]
        voice.play(discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(URL, **FFMPEG_OPTIONS), volume=soundvolume))

@bot.command(name="정지", aliases=["pause", "stop"])
async def pause(ctx):
    if not bot.voice_clients[0].is_paused():
        bot.voice_clients[0].pause()
        return
    em = discord.Embed(title="오류", description="이미 정지되어 있습니다", colour=color)
    await ctx.send(embed=em)

@bot.command(name="재시작", aliases=["ressume"])
async def resume(ctx):
    if bot.voice_clients[0].is_paused():
        bot.voice_clients[0].resume()
        return
    em = discord.Embed(title="오류", description="이미 재생 중 입니다", colour=color)
    await ctx.send(embed=em)

@bot.command(name="나가", aliases=["leave", "die"])
async def leave(ctx):
    await bot.voice_clients[0].disconnect()
    em = discord.Embed(title="성공", description="음성채널에서 나갔습니다", colour=color)
    await ctx.send(embed=em)

@bot.command(name="주사위")
async def dice(ctx):
    dice = random.choice([":one:이", ":two:가", ":three:이", ":four:가", ":five:가", ":six:이"])  # 뒤 글자도 써야함
    await ctx.send("데구르르... " + dice + " 나왔어요!")

@bot.command(name="날짜")
async def date(ctx):
    nowtime = datetime.date.today()
    await ctx.send(nowtime.strftime("20%y년 %m월 %d일 입니다."))

@bot.command(name="정보")
async def info(ctx):
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

@bot.command(name="유저정보")
async def usrinfo(ctx, member : discord.Member = None):
    if member == None:
        member = ctx.author
    userembed = discord.Embed(colour=color, title = member.display_name)
    userembed.set_thumbnail(url=member.avatar_url)
    userembed.add_field(name="계정명", value = member.name + "#" + member.discriminator)
    userembed.add_field(name="닉네임", value = member.display_name)
    userembed.add_field(name="ID", value=member.id)
    userembed.add_field(name="최상위 역할", value=member.top_role)
    userembed.add_field(name="계정 생성 날짜", value=member.created_at)
    await ctx.send(embed = userembed)

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

@bot.command(name = "급식")
async def food(ctx):
    em = discord.Embed(title="급식", description=_info.school_menu("양전초등학교"), colour=color)
    await ctx.send(embed=em)

@bot.command(name="날씨")
async def weather(ctx, *, content = "개포동"):
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
async def trans(ctx, inputlang, outputlang, *,content):
    result = translator.translate(content, src=inputlang, dest=outputlang)
    em = discord.Embed(title="번역", colour=color)
    em.add_field(name=f"Input({inputlang})", value=f"```\n{content}```")
    em.add_field(name=f"Output({outputlang})", value=f"```\n{result.text}```")
    em.set_footer(text="Powered by Google", icon_url="https://upload.wikimedia.org/wikipedia/commons/thumb/5/53/Google_%22G%22_Logo.svg/1200px-Google_%22G%22_Logo.svg.png")
    await ctx.send(embed=em)

@bot.command(name="도움")
async def helpcommand(ctx, section=""):
    if section == "":
        em = discord.Embed(title="도움말", colour=color)
        em.add_field(name="관리 명령", value="!도움 관리")
        em.add_field(name="음악 명령", value="!도움 음악")
        em.add_field(name="편의 명령", value="!도움 편의")
        em.add_field(name="번역 명령", value="!도움 번역")
        em.add_field(name="활동 명령", value="!도움 활동")
        em.add_field(name="기타 명령", value="!도움 기타")
    elif section == "관리":
        em = discord.Embed(title="관리 명령(관리자만 사용 가능)", colour=color)
        em.add_field(name="!k `멘션` `이유`", value="`멘션`유저를 킥합니다")
        em.add_field(name="!b `멘션` `이유`", value="`멘션`유저를 밴합니다")
        em.add_field(name="!m `멘션` `시간`", value="`멘션`유저를 `시간`만큼 뮤트합니다")
        em.add_field(name="!um `멘션`", value="`멘션`유저를 언뮤트합니다")
        em.add_field(name="!w `멘션` `이유`", value="`멘션`유저를 경고합니다")
        em.add_field(name="!uw `멘션`", value="`멘션`유저의 경고를 삭제합니다")
    elif section == "음악":
        em = discord.Embed(title="음악 명령", colour=color)
        em.add_field(name="!재생 `url`", value="`url`영상을 재생합니다", inline=False)
        em.add_field(name="!정지", value="재생중인 음악을 정지합니다", inline=False)
        em.add_field(name="!재시작", value="정지된 음악을 재생합니다", inline=False)
        em.add_field(name="!나가", value="음성채널에서 나갑니다", inline=False)
    elif section == "편의":
        em = discord.Embed(title="편의 명령", colour=color)
        em.add_field(name="!급식", value="급식을 알려줍니다", inline=False)
        em.add_field(name="!날씨 `위치`", value="`위치`의 날씨를 알려줍니다. `위치`에 아무것도 입력하지 않을 경우, 개포동의 날씨를 얄려줍니다", inline=False)
        em.add_field(name="!강아지", value="랜덤 강아지 짤을 보여줍니다", inline=False)
        em.add_field(name="!고양이", value="랜덤 고양이 짤을 보여줍니다", inline=False)
        em.add_field(name="!주사위", value="주사위를 던집니다", inline=False)
        em.add_field(name="!유저정보 `멘션`", value="`멘션`유저의 정보를 보여줍니다. `멘션`에 아무것도 입력하지 않을 경우, 자신의 정보를 알려줍니다", inline=False)
    elif section == "번역":
        em = discord.Embed(title="번역 명령", colour=color)
        em.add_field(name="!번역 `입력 언어` `출력 언어` `내용`", value="`내용`을 `입력 언어`에서 `출력 언어`로 번역합니다\
        \n주의:`입력 언어`와 `출력 언어`에는 언어 코드를 입력하세요", inline=False)
        em.add_field(name="언어 코드", value="```자동:auto\n한국어:ko\n영어:en\n일본어:ja\n프랑스어:fr```", inline=False)
    elif section == "기타":
        em = discord.Embed(title="기타 명령", colour=color)
        em.add_field(name="!정보", value="이 봇의 정보를 보여줍니다")
        em.add_field(name="!eval `코드`", value="`코드`를 실행합니다")
        em.add_field(name="!핑", value="이 봇의 핑을 알려줍니다")
        em.add_field(name="!건의 `내용`", value="<@!798690702635827200>에게 건의를 합니다")
    elif section == "활동":
        em = discord.Embed(title="활동 명령", colour=color)
        em.add_field(name="!유튜브", value="유튜브 투게더를 실행합니다")
        em.add_field(name="!체스", value="체스를 실행합니다")
        em.add_field(name="!포커", value="포커를 실행합니다")
        em.add_field(name="!낚시", value="낚시를 실행합니다")
        em.add_field(name="!모험", value="모험을 실행합니다")
    else:return
    await ctx.send(embed=em)

@bot.command(name="유튜브")
async def youtube_together(ctx):
    try:
        link = await togetherControl.create_link(ctx.author.voice.channel.id, 'youtube')
    except:
        em = discord.Embed(title="오류", description="음성채널에 들어가 주세요", colour=bad)
        await ctx.send(embed=em)
        return
    if ctx.author.voice.channel.id == 870820086930341930:
        await ctx.send(f"파란 글씨를 눌러주세요!\n{link}")
    else:
        em = discord.Embed(title="오류", description="<#870820086930341930> 음성채널에 들어가 주세요", colour = bad)
        await ctx.send(embed=em)

@bot.command(name="체스")
async def chess_together(ctx):
    try:
        link = await togetherControl.create_link(ctx.author.voice.channel.id, 'chess')
    except:
        em = discord.Embed(title="오류", description="음성채널에 들어가 주세요", colour=bad)
        await ctx.send(embed=em)
        return
    if ctx.author.voice.channel.id == 870820086930341930:
        await ctx.send(f"파란 글씨를 눌러주세요!\n{link}")
    else:
        em = discord.Embed(title="오류", description="<#870820086930341930> 음성채널에 들어가 주세요", colour = bad)
        await ctx.send(embed=em)

@bot.command(name="포커")
async def poker_together(ctx):
    try:
        link = await togetherControl.create_link(ctx.author.voice.channel.id, 'poker')
    except:
        em = discord.Embed(title="오류", description="음성채널에 들어가 주세요", colour=bad)
        await ctx.send(embed=em)
        return
    if ctx.author.voice.channel.id == 870820086930341930:
        await ctx.send(f"파란 글씨를 눌러주세요!\n{link}")
    else:
        em = discord.Embed(title="오류", description="<#870820086930341930> 음성채널에 들어가 주세요", colour = bad)
        await ctx.send(embed=em)

@bot.command(name="낚시")
async def poker_together(ctx):
    try:
        link = await togetherControl.create_link(ctx.author.voice.channel.id, 'fishing')
    except:
        em = discord.Embed(title="오류", description="음성채널에 들어가 주세요", colour=bad)
        await ctx.send(embed=em)
        return
    if ctx.author.voice.channel.id == 870820086930341930:
        await ctx.send(f"파란 글씨를 눌러주세요!\n{link}")
    else:
        em = discord.Embed(title="오류", description="<#870820086930341930> 음성채널에 들어가 주세요", colour = bad)
        await ctx.send(embed=em)

@bot.command(name="모험")
async def poker_together(ctx):
    try:
        link = await togetherControl.create_link(ctx.author.voice.channel.id, 'betrayal')
    except:
        em = discord.Embed(title="오류", description="음성채널에 들어가 주세요", colour=bad)
        await ctx.send(embed=em)
        return
    if ctx.author.voice.channel.id == 870820086930341930:
        await ctx.send(f"파란 글씨를 눌러주세요!\n{link}")
    else:
        em = discord.Embed(title="오류", description="<#870820086930341930> 음성채널에 들어가 주세요", colour = bad)
        await ctx.send(embed=em)

@bot.command(name="건의")
async def dmtodev(ctx, *, content:str):
    embed = discord.Embed(colour=color, title = "건의")
    embed.add_field(name="건의자", value = f"{ctx.author.name}#{ctx.author.discriminator}({ctx.author.id})", inline=False)
    embed.add_field(name="내용", value = content, inline=False)
    devdm = await bot.fetch_user(798690702635827200)
    await devdm.send(embed=embed)

"""
@bot.command(name="검색")
async def youtube_shearch(ctx, *, content):
    query = urllib.parse.quote(content)
    hdr = {'User-Agent': (
        'mozilla/5.0 (windows nt 10.0; win64; x64) applewebkit/537.36 (khtml, like gecko) chrome/78.0.3904.70 safari/537.36')}
    webpage = requests.get(f"https://www.youtube.com/results?search_query={query}", headers=hdr)
    print(f"https://www.youtube.com/results?search_query={query}")
    soup = BeautifulSoup(webpage.content, "html.parser")
    start = str(soup).find("href=\"/watch?v=") + 6
    print(start)
    end = str(soup).find("\"><yt-img-shadow ftl-eligible=\"\" class=\"style-scope ytd-thumbnail no-transition\" style=\"background-color: transparent;\"")
    print(end)
    print(str(soup)[start:end])
"""

@bot.event
async def on_message(message):
    msgcontent = message.content
    bad = 0
    for x in range(0, len(badwords)):
        bad = bad + msgcontent.find(badwords[x]) + 1
    if bad != 0:
        badembed = discord.Embed(title=":no_entry_sign:욕설/금지어 사용 경고:no_entry_sign:", description=str(message.author.mention) \
            + "님이 욕설/금지어를 사용하셨습니다.", colour = color)
        await message.delete()
        await message.channel.send(embed=badembed)
    await bot.process_commands(message)

@bot.event
async def on_member_join(member):
    await member.add_roles(member.guild.get_role(859237801898803210), reason="서버에 들어옴")
    embed=discord.Embed(title="환영합니다!", description=f"{member.mention}님 **양전초 서버**에 오신 것을 환영합니다!", color=color, timestamp=datetime.datetime.utcnow())
    embed.set_thumbnail(url=member.avatar_url)
    embed.set_footer(text=member)
    embed.add_field(name="시간", value = f"<t:{math.trunc(time.time())}:R>")
    await bot.get_channel(842729679395356712).send(embed=embed)

@bot.event
async def on_member_remove(member):
    embed=discord.Embed(title="멤버 퇴장/강퇴", description=f"{member.mention}님이 서버에서 퇴장/강퇴 되었습니다", color=color, timestamp=datetime.datetime.utcnow())
    embed.set_thumbnail(url=member.avatar_url)
    embed.set_footer(text=member)
    embed.add_field(name="시간", value = f"<t:{math.trunc(time.time())}:R>")
    await bot.get_channel(842729679395356712).send(embed=embed)

bot.run(token)