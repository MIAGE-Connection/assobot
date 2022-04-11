import discord
from discord.ext import commands

from assobot.core.plugin import AbstractPlugin
from assobot.core.utils.logger import get_logger
from .core import *

LOGGER = get_logger(__name__)

class welcomePlugin(AbstractPlugin):

    def __init__(self) -> None:
        super().__init__('welcome', 'Allow bot to welcoming new members')

    @commands.command()
    async def hello(self, ctx):
        settings_manager = self.get_settings_manager(ctx.guild)
        if not bool(settings_manager.get("enabled")): return
        await ctx.channel.send(settings_manager.get("hello-message"))

    @commands.Cog.listener()
    async def on_member_join(self, member):
        settings_manager = self.get_settings_manager(member.guild)
        if not bool(settings_manager.get("enabled")): return
        
        id = int(settings_manager.get('welcome-message-channel'))

        welcome_channel = discord.utils.get(member.guild.channels, id=id)
        welcome_message = settings_manager.get('welcome-message')

        if welcome_channel:
            await welcome_channel.send(welcome_message)
        else:
            LOGGER.error(f"Error : no channel with ID {id}")
            return