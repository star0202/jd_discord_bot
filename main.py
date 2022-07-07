import discord
from discord.ext import commands
import time
import os
from auth import token
from config import status

bot = commands.Bot(command_prefix="v!", intents = discord.Intents.all(), help_command=None)
bot.start_time = time.time()


@bot.event
async def on_ready():
    print("Log In")
    channel = await bot.fetch_channel(992637152527667210)
    await channel.send(f"{bot.user.mention} 시작됨")
    await bot.change_presence(
        status=discord.Status.online,
        activity=discord.Game(status),
    )
for filename in os.listdir("functions"):
    if filename.endswith(".py"):
        bot.load_extension(f"functions.{filename[:-3]}")
print(f"{len(bot.extensions)} extensions loaded)")

bot.run(token)
