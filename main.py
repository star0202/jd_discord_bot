import discord
from discord.ext import commands
import time
import os
from auth import token

bot = commands.Bot(command_prefix="/", intents = discord.Intents.all(), help_command=None)
bot.start_time = time.time()


@bot.event
async def on_ready():
    await bot.change_presence(
        status=discord.Status.online,
        activity=discord.Game(f"테스팅 중"),
    )
for filename in os.listdir("functions"):
    if filename.endswith(".py"):
        bot.load_extension(f"functions.{filename[:-3]}")


bot.run(token)
