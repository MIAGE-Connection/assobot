from assobot import CLIENT
from assobot.core.auth.auth_manager import LOGGER
import discord
from discord.ext import commands
import emojis
from discord.ext.commands import has_permissions

from assobot.core.plugin import AbstractPlugin


class reaction_rolePlugin(AbstractPlugin):

    def __init__(self) -> None:
        super().__init__('Reaction_Role', 'Give roles on member reactions')

    @has_permissions(administrator=True)
    @commands.command(name='reaction_role')
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
                    LOGGER.error("Member not found")
            else:
                LOGGER.error("Role not found")

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
                LOGGER.error("Member not found")
        else:
            LOGGER.error("Role not found")

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

    def get_role_from_emoji(self, payload, guild):
        settings_manager = self.get_settings_manager(guild)
        emoji_list = settings_manager.get('reaction-emoji-groups')
        role_list = settings_manager.get('reaction-role-groups')
        index = emoji_list.index(emojis.decode(payload.emoji.name))
        return discord.utils.get(guild.roles, id=int(role_list[index]))
