import emojis

from assobot.core.auth.auth_manager import LOGGER
import discord
from discord.ext import commands
from discord.ext.commands import has_permissions

from assobot.core.plugin import AbstractPlugin


class reaction_rolePlugin(AbstractPlugin):

    def __init__(self) -> None:
        super().__init__('reaction_role', 'Laissez vos membres obtenir un rôle en réagissant à un message.')

    @has_permissions(administrator=True)
    @commands.command(name='display_reaction_message')
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
                    await self.try_to_add_or_remove_role(guild, member, role, payload.channel_id, False)
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
                await self.try_to_add_or_remove_role(guild, member, role, payload.channel_id, True)
            else:
                LOGGER.error("Member not found")
        else:
            LOGGER.error("Role not found")

    async def send_reaction_role_message(self, ctx):
        settings_manager = self.get_settings_manager(ctx.guild)
        channel_id = int(settings_manager.get('reaction-role-channel'))

        reaction_role_channel = discord.utils.get(ctx.guild.channels, id=channel_id)

        reaction_role_message = self.add_role_reaction_to_message(settings_manager, ctx.guild,
                                                                  settings_manager.get('reaction-role-message'))

        if reaction_role_channel is None: return
        
        sended_reaction_role_message = await reaction_role_channel.send(reaction_role_message)
        await self.add_all_reactions_to_message(settings_manager, sended_reaction_role_message)

        settings_manager.set('reaction-role-message-id', sended_reaction_role_message.id)
        settings_manager.save()

    async def add_all_reactions_to_message(self, settings_manager, message):
        emoji_list = settings_manager.get('reaction-emoji-groups')
        for emoji in emoji_list:
            await message.add_reaction(emojis.encode(emoji))

    def get_role_from_emoji(self, payload, guild):
        settings_manager = self.get_settings_manager(guild)
        emoji_list = settings_manager.get('reaction-emoji-groups')
        role_list = settings_manager.get('reaction-role-groups')
        index = emoji_list.index(emojis.decode(payload.emoji.name))
        return discord.utils.get(guild.roles, id=int(role_list[index]))

    def add_role_reaction_to_message(self, settings_manager, guild, reaction_role_message):
        emoji_list = settings_manager.get('reaction-emoji-groups')
        role_list = settings_manager.get('reaction-role-groups')
        for index, emoji in enumerate(emoji_list):
            role = discord.utils.get(guild.roles, id=int(role_list[index]))
            reaction_role_message += f'\n \t - {emoji} : {role.name}'
        return reaction_role_message

    async def try_to_add_or_remove_role(self, guild, member, role, channel_id, remove):
        try:
            if remove:
                await member.remove_roles(role)
            else:
                await member.add_roles(role)
        except:
            if remove:
                participe_passe = 'retiré'
            else:
                participe_passe = 'attribué'
            error_message = f'Le role {role.name} ne peut pas être {participe_passe} car le role Assobot n\' est pas assez haut dans la hierarchie des rôles veuillez contacter un admin'
            channel = discord.utils.get(guild.channels, id=channel_id)
            await channel.send(error_message)