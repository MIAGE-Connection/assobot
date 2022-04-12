import discord
from discord.ext import commands

from assobot import BOT
from assobot.core.plugin import AbstractPlugin
from .core import *

class reaction_rolePlugin(AbstractPlugin):

    def __init__(self) -> None:
        super().__init__('Reaction_Role', 'Give roles on member reactions')

    @commands.command()
    async def hello_reaction_role(self, ctx):
        settings_manager = self.get_settings_manager(ctx.guild)
        if not bool(settings_manager.get("enabled")): return
        await ctx.channel.send(settings_manager.get("hello-message"))