import discord
import logging
from discord.ext import commands
import time
import os
from auth import token
from config import STATUS
import utils.logger


utils.logger.setup_logging()
logger = logging.getLogger("main")


class Viridian(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix="v!", intents=discord.Intents.all(), help_command=None)
        for filename in os.listdir("functions"):
            if filename.endswith(".py"):
                self.load_extension(f"functions.{filename[:-3]}")
        logger.info(f"{len(self.extensions)} extensions are completely loaded")

    async def on_ready(self):
        logger.info(f"Logged in as {bot.user.name}")
        await self.change_presence(
            status=discord.Status.online,
            activity=discord.Game(STATUS),
        )


bot = Viridian()
bot.start_time = time.time()
bot.load_extension('jishaku')

bot.run(token)
