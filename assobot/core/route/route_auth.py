
from assobot.config import REDIRECT_URL
from flask import *

from zenora import APIClient
from assobot import APP, CLIENT, REDIRECT_OAUTH_URL, CURRENT_USER


@APP.route('/login')
def guild_list():
    if 'token' in session:
        bearer_client = APIClient(session.get('token'), bearer=True)
        CURRENT_USER = bearer_client.users.get_current_user()
        user_guilds = list()
        for guild in bearer_client.users.get_my_guilds():
            if (int(guild.permissions) & 8) == 8:
                user_guilds.append(guild)
        return render_template('default/guilds.html', current_user=CURRENT_USER, guilds=user_guilds)
    return render_template('default/auth/login.html', redirect_oauth_uri=REDIRECT_OAUTH_URL)

@APP.route('/logout')
def logout():
    session.clear()
    return redirect("/")

@APP.route('/oauth/callback')
def callback():
    code = request.args['code']
    access_token = CLIENT.oauth.get_access_token(code, REDIRECT_URL).access_token
    session['token'] = access_token
    return redirect("/login")
