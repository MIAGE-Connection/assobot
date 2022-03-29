from assobot import APP, BOT, DISCORD_BOT_TOKEN
from .plugins import bot_commands as cmd, member_join_plugin as mjp
from flask import render_template
from threading import Thread
from functools import partial
import discord

@APP.route("/")
def home():
   return render_template('index.html')

def addAllDefaultCommands():
    BOT.add_command(cmd.hello)
    BOT.add_command(cmd.delete)

def addAllDefaultPlugins():
    BOT.add_listener(mjp.on_member_join, 'on_member_join')

def launch():
    partial_run = partial(APP.run, host="127.0.0.1", port=5000, debug=True, use_reloader=False)
    Thread(target=partial_run).start()
    addAllDefaultCommands()
    addAllDefaultPlugins()
    BOT.run(DISCORD_BOT_TOKEN)