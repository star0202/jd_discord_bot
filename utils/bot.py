from discord.ext import commands
import logging
import discord
from datetime import timedelta
from time import time
from config import STATUS, TEST_GUILD_ID
from utils.logger import setup_logging
import os
import sys
from traceback import format_exception
from config import BAD, MESSAGE_LOGGING, COLOR
from utils.timeconvert import datetime_to_unix


class Viridian(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix="v!", intents=discord.Intents.all(), help_command=None,
                         debug_guilds=[TEST_GUILD_ID])
        setup_logging()
        self.logger = logging.getLogger(__name__)
        self.start_time = time()
        for filename in os.listdir("functions"):
            if filename.endswith(".py"):
                self.load_cog(f"functions.{filename[:-3]}")
        self.logger.info(f"{len(self.extensions)} extensions are completely loaded")
        self.load_extension('jishaku')

    def load_cog(self, cog: str):
        try:
            if type(self.load_extension(cog)[cog]) == discord.ExtensionFailed:
                self.logger.error(self.load_extension(cog)[cog])
        except Exception as e:
            self.logger.error(e)

    def run(self):
        super().run(os.getenv("TOKEN"))

    async def on_ready(self):
        self.logger.info(f"Logged in as {self.user.name}")
        await self.change_presence(
            status=discord.Status.online,
            activity=discord.Game(STATUS),
        )
        await self.wait_until_ready()

    async def on_command_error(self, ctx: commands.Context, error: commands.CommandError):
        text = "".join(format_exception(type(error), error, error.__traceback__))
        self.logger.error(text)
        await ctx.send(
            embed=discord.Embed(
                title=f"오류 발생: {error.__class__.__name__}",
                description=f"```{text}```",
                color=BAD
            )
        )

    async def on_message_edit(self, before: discord.Message, after: discord.Message):
        channel = await self.fetch_channel(MESSAGE_LOGGING)
        embed = discord.Embed(title="메세지 수정됨", color=COLOR)
        embed.add_field(name="수정 전", value=f"```{before.content}```")
        embed.add_field(name="수정 후", value=f"```{after.content}```")
        embed.add_field(name="보낸 유저", value=after.author.mention)
        embed.add_field(name="채널", value=after.channel.mention)
        embed.add_field(name="메세지 링크", value=after.jump_url)
        embed.add_field(name="수정된 시각", value=f"<t:{datetime_to_unix(after.edited_at+timedelta(hours=9))}:R>")
        await channel.send(embed=embed)

    async def on_message_delete(self, message: discord.Message):
        channel = await self.fetch_channel(MESSAGE_LOGGING)
        embed = discord.Embed(title="메세지 삭제됨", color=BAD)
        embed.add_field(name="내용", value=f"```{message.content}```")
        embed.add_field(name="보낸 유저", value=message.author.mention)
        embed.add_field(name="채널", value=message.channel.mention)
        await channel.send(embed=embed)

    async def on_error(self, event, *args, **kwargs):
        error = sys.exc_info()
        text = f"{error[0].__name__}: {error[1]}"
        embed = discord.Embed(title=f'오류 발생: {error[0].__name__}', color=BAD, description=f"```{text}```")
        await args[0].channel.send(embed=embed)
        text = text.replace("\n", " | ")
        self.logger.error(text)
