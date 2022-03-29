from flask import Flask
from .config import DISCORD_BOT_TOKEN
import discord
from discord.ext import commands
import sys

sys.dont_write_bytecode = True

APP = Flask(__name__)
BOT = commands.Bot(command_prefix='>', intents=discord.Intents.all())

from .plugins import bot_commands, member_join_plugin

@BOT.event
async def on_connect():
    print("The BOT have started !")