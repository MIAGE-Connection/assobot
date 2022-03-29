from discord.ext import commands
import discord

@commands.Cog.listener()
async def on_member_join(member):
    id = 956168238729953281
    welcome_channel = discord.utils.get(member.guild.channels, id=id)
    if not welcome_channel:
        print(f"Error : no channel with ID {id}")
        return
    else:
        await welcome_channel.send(f"Bienvenue sur le serveur {member.mention} !")