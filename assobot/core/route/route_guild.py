from assobot import APP, CURRENT_USER
from flask import *
from zenora import APIClient

def getGuildById(guilds, idGuild):
    for guild in guilds:
        if str(guild.id) == idGuild:
            return guild

@APP.route('/guild/<idGuild>')
def guild_manage(idGuild=None):
    if 'token' in session and idGuild:
        bearer_client = APIClient(session.get('token'), bearer=True)
        CURRENT_USER = bearer_client.users.get_current_user()
        guild_user = getGuildById(bearer_client.users.get_my_guilds(), idGuild)
        return render_template('default/plugin/plugin_list.html', current_user=CURRENT_USER, guild=guild_user)
