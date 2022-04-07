from flask import *
from zenora import APIClient

from assobot import APP, AUTH_MANAGER, CLIENT, REDIRECT_OAUTH_URL, REDIRECT_URL

@APP.route('/login')
def login():
    if 'token' in session:
        AUTH_MANAGER.create_auth(session['token'])
        return redirect('/guilds')
    return render_template('default/auth/login.html', redirect_oauth_uri=REDIRECT_OAUTH_URL)

@APP.route('/logout')
def logout():
    if 'token' in session:
        AUTH_MANAGER.remove_auth(session['token'])
        session.clear()
    return redirect("/")

@APP.route('/oauth/callback')
def callback():
    code = request.args['code']
    access_token = CLIENT.oauth.get_access_token(code, REDIRECT_URL).access_token
    session['token'] = access_token
    AUTH_MANAGER.create_auth(session['token'])
    return redirect("/login")

def current_user_function():
    CURRENT_USER = None
    if 'token' in session :
        bearer_client = APIClient(session.get('token'), bearer=True)
        CURRENT_USER = bearer_client.users.get_current_user()
    return CURRENT_USER

@APP.context_processor
def context_processor():
    return dict(current_user=current_user_function)