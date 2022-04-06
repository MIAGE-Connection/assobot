from flask import *

from assobot import APP, CLIENT, REDIRECT_OAUTH_URL, REDIRECT_URL

@APP.route('/login')
def login():
    if 'token' in session:
        return redirect('/guilds')
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
