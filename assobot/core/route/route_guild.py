from assobot import APP, CURRENT_USER
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

    user_guilds = list()
    for guild in bearer_client.users.get_my_guilds():
            if (int(guild.permissions) & 8) == 8:
                user_guilds.append(guild)
    
    return render_template('default/guilds.html', current_user=bearer_client.users.get_current_user(), guilds=user_guilds)


@APP.route('/guild/<idGuild>')
def guild_manage(idGuild=None):
    if 'token' in session and idGuild:
        bearer_client = APIClient(session.get('token'), bearer=True)
        CURRENT_USER = bearer_client.users.get_current_user()
        guild_user = getGuildById(bearer_client.users.get_my_guilds(), idGuild)
        return render_template('default/plugin/plugin_list.html', current_user=CURRENT_USER, guild=guild_user)
