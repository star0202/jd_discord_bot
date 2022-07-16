import discord
import logging
from discord.ext import commands
import time
import os
from auth import token
from config import STATUS
import utils.logger

bot = commands.Bot(command_prefix="v!", intents=discord.Intents.all(), help_command=None)
bot.start_time = time.time()
bot.load_extension('jishaku')
utils.logger.setup_logging()
logger = logging.getLogger("main")


@bot.event
async def on_ready():
    logger.info(f"Logged in as {bot.user.name}")
    await bot.change_presence(
        status=discord.Status.online,
        activity=discord.Game(STATUS),
    )
for filename in os.listdir("functions"):
    if filename.endswith(".py"):
        bot.load_extension(f"functions.{filename[:-3]}")
logger.info(f"{len(bot.extensions)} extensions are completely loaded")

bot.run(token)
