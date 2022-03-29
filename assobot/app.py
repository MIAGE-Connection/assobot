from flask import Flask, render_template, request, session, redirect

from assobot.config import TOKEN, CLIENT_SECRET, REDIRECT_OAUTH_URL, REDIRECT_URL
from zenora import APIClient

app = Flask(__name__)
app.config["SECRET_KEY"] = "e5676d216b52c91d0c96750f781f445b730fd76f14315cc6358f7f647554f454"
client = APIClient(TOKEN, client_secret=CLIENT_SECRET)

@app.route("/")
def home():
    if 'token' in session:
        bearer_client = APIClient(session.get('token'), bearer=True)
        current_user = bearer_client.users.get_current_user()
        user_guilds = list()
        for guild in bearer_client.users.get_my_guilds():
            if (int(guild.permissions) & 8) == 8:
                user_guilds.append(guild)
        return render_template('index.html', current_user=current_user, guilds=user_guilds)
    return render_template('index.html', redirect_oauth_uri=REDIRECT_OAUTH_URL)

@app.route("/oauth/callback")
def callback():
    code = request.args['code']
    access_token = client.oauth.get_access_token(code, REDIRECT_URL).access_token
    session['token'] = access_token
    return redirect("/")

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

def launch():
    app.run()