import discord

from assobot import APP, BOT, CURRENT_USER, PARTIAL_URL_BOT_ADD, PLUGIN_MANAGER
from flask import *
from zenora import APIClient


def getGuildById(guilds, idGuild):
    for guild in guilds:
        if str(guild.id) == idGuild:
            return guild


@APP.route('/guilds')
def guild_list():
    if not 'token' in session: return
    
    bearer_client = APIClient(session.get('token'), bearer=True)

    not_joined_guilds = list()
    joined_guilds = list()
    for guild in bearer_client.users.get_my_guilds():
            if (int(guild.permissions) & 8) == 8:
                if (has_already_join(guild.id)):
                    joined_guilds.append(guild)
                else:
                    not_joined_guilds.append(guild)
    
    return render_template('default/guilds.html', current_user=bearer_client.users.get_current_user(), guilds_not_joined=not_joined_guilds, guilds_joined=joined_guilds, partial_url=PARTIAL_URL_BOT_ADD)


@APP.route('/guild/<idGuild>')
def guild_manage(idGuild=None):
    if 'token' in session and idGuild:
        bearer_client = APIClient(session.get('token'), bearer=True)
        CURRENT_USER = bearer_client.users.get_current_user()
        guild_user = getGuildById(bearer_client.users.get_my_guilds(), idGuild)
        return render_template('default/plugin/plugin_list.html', current_user=CURRENT_USER, guild=guild_user, plugins=list(PLUGIN_MANAGER.plugins.values()))

@APP.route('/guild/callback')
def callback_guild():
    guild_id = request.args['guild_id']
    return redirect(f"/guild/{guild_id}")

def has_already_join(guild_id):
    guild = BOT.get_guild(guild_id)
    if guild is not None and guild.members is not None:
        return True
    else:
        return False
