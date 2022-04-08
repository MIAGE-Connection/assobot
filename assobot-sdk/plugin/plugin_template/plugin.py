import discord
from discord.ext import commands

from assobot import BOT
from assobot.core.plugin import AbstractPlugin
from .core import *

class [[PLUGIN_NAME]]Plugin(AbstractPlugin):

    def __init__(self, install_path) -> None:
        super().__init__('[[PLUGIN_NAME]]', '[[PLUGIN_DESCRIPTION]]', install_path)

    @commands.command()
    async def hello(self, ctx):
        settings_manager = self.get_settings_manager(ctx.guild)
        if not bool(settings_manager.get("enabled")): return
        await ctx.channel.send(settings_manager.get("hello-message"))