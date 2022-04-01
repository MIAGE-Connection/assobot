import discord
from discord.ext import commands

from assobot import BOT
from assobot.core.plugin import AbstractPlugin
from .core import *

class [[PLUGIN_NAME]]Plugin(AbstractPlugin):

    def __init__(self) -> None:
        super().__init__('[[PLUGIN_NAME]]', '[[PLUGIN_DESCRIPTION]]')

    @commands.command()
    async def hello(self, ctx):
        if not self.enabled: return
        await ctx.channel.send(self.settings.get("hello-message"))