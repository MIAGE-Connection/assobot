from assobot import CLIENT
import discord
from discord.ext import commands
import emojis
from discord.ext.commands import has_permissions

from assobot.core.plugin import AbstractPlugin
from .core import *


class reaction_rolePlugin(AbstractPlugin):

    def __init__(self) -> None:
        super().__init__('Reaction_Role', 'Give roles on member reactions')

    @has_permissions(administrator=True)
    @commands.command(name='rr')
    async def invoke_reaction_role_message(self, ctx):
        settings_manager = self.get_settings_manager(ctx.guild)
        if not bool(settings_manager.get("enabled")): return
        message_id = int(settings_manager.get("reaction-role-message-id"))
        if message_id != -1:
            id_role_channel = int(settings_manager.get("reaction-role-channel"))
            if (id_role_channel != -1):
                reaction_role_channel = discord.utils.get(ctx.guild.channels, id=id_role_channel)
                try:
                    msg = await reaction_role_channel.fetch_message(message_id)
                    await msg.delete()
                except:
                    pass
        await ctx.message.delete()
        await self.send_reaction_role_message(ctx)

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        if not payload.member.bot:
            guild = discord.utils.find(lambda g: g.id == payload.guild_id, self.bot.guilds)

            settings_manager = self.get_settings_manager(guild)
            if not bool(settings_manager.get("enabled")): return

            id_role_channel = int(settings_manager.get("reaction-role-channel"))
            if (id_role_channel != payload.channel_id): return

            id_role_message = int(settings_manager.get("reaction-role-message-id"))
            if (id_role_message != payload.message_id): return

            role = self.get_role_from_emoji(payload, guild)

            if role is not None:
                member = payload.member
                if member is not None:
                    await member.add_roles(role)
                else:
                    print("member not found")
            else:
                print("role not found")

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):
        guild = discord.utils.find(lambda g: g.id == payload.guild_id, self.bot.guilds)
        member = discord.utils.find(lambda m: m.id == payload.user_id, guild.members)

        settings_manager = self.get_settings_manager(guild)
        if not bool(settings_manager.get("enabled")): return

        id_role_channel = int(settings_manager.get("reaction-role-channel"))
        if (id_role_channel != payload.channel_id): return

        id_role_message = int(settings_manager.get("reaction-role-message-id"))
        if (id_role_message != payload.message_id): return

        role = self.get_role_from_emoji(payload, guild)

        if role is not None:
            if member is not None:
                await member.remove_roles(role)
            else:
                print("member not found")
        else:
            print("role not found")

    async def send_reaction_role_message(self, ctx):
        settings_manager = self.get_settings_manager(ctx.guild)
        channel_id = int(settings_manager.get('reaction-role-channel'))

        reaction_role_channel = discord.utils.get(ctx.guild.channels, id=channel_id)

        reaction_role_message = settings_manager.get('reaction-role-message')

        sended_reaction_role_message = await reaction_role_channel.send(reaction_role_message)
        await self.add_all_reactions_to_message(ctx.guild, settings_manager, sended_reaction_role_message)

        settings_manager.set('reaction-role-message-id', sended_reaction_role_message.id)
        settings_manager.save()

    async def add_all_reactions_to_message(self, guild, settings_manager, message):
        emoji_name = settings_manager.get('reaction-emoji')
        await message.add_reaction(emojis.encode(emoji_name))

    def get_role_from_emoji(self, payload, guild):
        settings_manager = self.get_settings_manager(guild)
        reaction_role_name = settings_manager.get('reaction-role')
        for role in guild.roles:
            if role.name == reaction_role_name:
                return role
        return None