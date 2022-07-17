import discord
import logging
from discord.ext import commands
from time import time
import os
from config import STATUS
import utils.logger
from dotenv import load_dotenv


utils.logger.setup_logging()
load_dotenv(".env")
logger = logging.getLogger("main")


class Viridian(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix="v!", intents=discord.Intents.all(), help_command=None)
        for filename in os.listdir("functions"):
            if filename.endswith(".py"):
                self.load_extension(f"functions.{filename[:-3]}")
        logger.info(f"{len(self.extensions)} extensions are completely loaded")
        self.start_time = time()
        self.load_extension('jishaku')

    async def on_ready(self):
        logger.info(f"Logged in as {self.user.name}")
        await self.change_presence(
            status=discord.Status.online,
            activity=discord.Game(STATUS),
        )


bot = Viridian()
bot.run(os.getenv("TOKEN"))
