import discord
from discord.ext import commands
import emoji
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
            if (id_role_message != payload.message_id):return

            role = self.get_role_from_emoji(payload, guild)

            if role is not None:
                print(role)
                member = payload.member
                if member is not None:
                    await member.add_roles(role)
                    print("done")
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

        await self.add_all_reactions_to_message(settings_manager, sended_reaction_role_message)

        settings_manager.set('reaction-role-message-id', sended_reaction_role_message.id)
        settings_manager.save()

    async def add_all_reactions_to_message(self, settings_manager, message):
        list_roles_emojis = settings_manager.get('roles_emoji')
        for role_emoji in list_roles_emojis:
            await message.add_reaction(role_emoji['emoji_name'])

    @has_permissions(administrator=True)
    @commands.command(name='del')
    async def delete_message(self, ctx):
        await ctx.message.channel.purge(limit=2)

    def get_role_from_emoji(self, payload, guild):
        settings_manager = self.get_settings_manager(guild)
        list_roles_emojis = settings_manager.get('roles_emoji')
        role = None
        for role_emoji in list_roles_emojis:
            emoji_name = role_emoji['emoji_name']
            emoji_name = emoji_name[emoji_name.find(':')+1:emoji_name.rfind(':')]
            print(emoji_name + ' ' + payload.emoji.name)
            if role_emoji['emoji_name'] == payload.emoji.name or emoji_name == payload.emoji.name:
                role = discord.utils.get(guild.roles, id=int(role_emoji['role_id']))
        return role