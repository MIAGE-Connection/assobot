import os
from functools import partial
from pathlib import *
from threading import Thread

import discord
from flask import *

from assobot import APP, BOT, BOT_SECRET, CLIENT_SECRET, REDIRECT_OAUTH_URL, REDIRECT_URL
from assobot.core.auth import *
from assobot.core.utils.logger import get_logger

LOGGER = get_logger(__name__)

APP.config["SECRET_KEY"] = "e5676d216b52c91d0c96750f781f445b730fd76f14315cc6358f7f647554f454"

UPLOAD_FOLDER = os.path.dirname(os.path.realpath(__file__))

@APP.route('/')
def home():
   return render_template('default/index.html', redirect_oauth_uri=REDIRECT_OAUTH_URL)

@APP.route('/guild/<idGuild>')
def guild_manage(idGuild=None):
    if 'token' in session and idGuild:
        bearer_client = APIClient(session.get('token'), bearer=True)
        current_user = bearer_client.users.get_current_user()
        guild_user = getGuildById(bearer_client.users.get_my_guilds(), idGuild)
        return render_template('default/plugin/plugin_list.html', current_user=current_user, guild=guild_user)

def launch():
   LOGGER.info('START Assobot Application')
   partial_run = partial(APP.run, host="127.0.0.1", port=5000, debug=True, use_reloader=False)
   Thread(target=partial_run).start()
   BOT.run(BOT_SECRET)
   LOGGER.info('STOP Assobot Application')

def getGuildById(guilds, idGuild):
    for guild in guilds:
        if str(guild.id) == idGuild:
            return guild
