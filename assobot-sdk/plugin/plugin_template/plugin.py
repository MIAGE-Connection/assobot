import discord
from discord.ext import commands

from assobot.core.plugin import AbstractPlugin
from .core import *

class Plugin(AbstractPlugin):

    def __init__(self) -> None:
        super().__init__('[[PLUGIN_NAME]]', '[[PLUGIN_DESCRIPTION]]')
        self.__add_commands()

    def __add_commands(self):
        self.bot.add_command(self.hello_world)

    @commands.command()
    async def hello_world(self, ctx, *args):
        if not self.enabled: return
        await ctx.channel.send(self.settings.get("hello-message"))