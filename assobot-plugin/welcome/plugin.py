import discord
from discord.ext import commands

from assobot.core.plugin import AbstractPlugin
from .core import *

class welcomePlugin(AbstractPlugin):

    def __init__(self) -> None:
        super().__init__('welcome', 'Allow bot to welcoming new members')

    @commands.command()
    async def hello(self, ctx):
        settings_manager = self.get_settings_manager(ctx.guild)
        if not bool(settings_manager.get("enabled")): return
        await ctx.channel.send(settings_manager.get("hello-message"))