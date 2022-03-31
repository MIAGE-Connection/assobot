import os
import uuid
from functools import partial
from pathlib import *
from threading import Thread

import discord
from flask import *
from werkzeug.utils import secure_filename
from zenora import APIClient

from assobot import APP, BOT, BOT_SECRET, TMP_FOLDER_PLUGIN, CLIENT_SECRET, REDIRECT_OAUTH_URL, REDIRECT_URL
from assobot.core.plugin.plugin_manager import PluginManager
from assobot.core.utils.logger import get_logger

LOGGER = get_logger(__name__)

APP.config["SECRET_KEY"] = "e5676d216b52c91d0c96750f781f445b730fd76f14315cc6358f7f647554f454"
client = APIClient(BOT_SECRET, client_secret=CLIENT_SECRET)

UPLOAD_FOLDER = os.path.dirname(os.path.realpath(__file__))
ALLOWED_EXTENSIONS = set(['zip'])

manager = PluginManager()

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@APP.route('/plugins/upload', methods=['GET', 'POST'])
def pluginsUpload():

   if request.method == 'POST':
      if 'file' not in request.files:
         return redirect('/')

      file = request.files['file']

      if file.filename == '':
         return redirect(request.url)

      if file and allowed_file(file.filename):
         filename = secure_filename(file.filename)
         dst_file_path = Path(os.path.join(TMP_FOLDER_PLUGIN, filename))
         file.save(dst_file_path)
         manager.load_plugin(dst_file_path)

   return render_template('default/index.html', plugins=list(manager.plugins.values()))

@APP.route('/plugin/<plugin_id>/settings')
def open_plugin_settings(plugin_id):
   plugin = manager.plugins.get(uuid.UUID(plugin_id), None)
   
   if plugin is None:
      return redirect('/')

   return render_template(f"plugins/{plugin.namespace}/settings.html", plugin=plugin)

@APP.route('/plugin/<plugin_id>/settings/update',  methods=['POST'])
def update_plugin_settings(plugin_id):
   plugin = manager.plugins.get(uuid.UUID(plugin_id), None)
      
   if plugin is None:
      return redirect('/')

   data = request.form.to_dict(flat=False)

   plugin.settings.update(data)

   return redirect(f'/plugin/{plugin.id}/settings')

@APP.route('/plugin/<plugin_id>/remove')
def remove_plugin(plugin_id):
   plugin = manager.plugins.get(uuid.UUID(plugin_id), None)
   
   if plugin is None:
      redirect('/')

   manager.unload_plugin(plugin)

   return redirect('/')

@APP.route('/plugin/<plugin_id>/enabled')
def enable_plugin(plugin_id):
   plugin = manager.plugins.get(uuid.UUID(plugin_id), None)
   
   if plugin is None:
      redirect('/')

   plugin.enabled = True

   return redirect('/')

@APP.route('/plugin/<plugin_id>/disabled')
def disable_plugin(plugin_id):
   plugin = manager.plugins.get(uuid.UUID(plugin_id), None)
   
   if plugin is None:
      redirect('/')

   plugin.enabled = False

   return redirect('/')

@APP.route('/')
def showGuilds():
    if 'token' in session:
        bearer_client = APIClient(session.get('token'), bearer=True)
        current_user = bearer_client.users.get_current_user()
        user_guilds = list()
        for guild in bearer_client.users.get_my_guilds():
            if (int(guild.permissions) & 8) == 8:
                user_guilds.append(guild)
        return render_template('default/guilds.html', current_user=current_user, guilds=user_guilds)
    return render_template('default/login.html', redirect_oauth_uri=REDIRECT_OAUTH_URL)


@APP.route('/guild/<idGuild>')
def pluginGallery(idGuild=None):
    if 'token' in session and idGuild:
        bearer_client = APIClient(session.get('token'), bearer=True)
        current_user = bearer_client.users.get_current_user()
        guild_user = getGuildById(bearer_client.users.get_my_guilds(), idGuild)
        return render_template('default/plugins.html', current_user=current_user, guild=guild_user)


@APP.route('/oauth/callback')
def callback():
    code = request.args['code']
    access_token = client.oauth.get_access_token(code, REDIRECT_URL).access_token
    session['token'] = access_token
    return redirect("/")


@APP.route('/logout')
def logout():
    session.clear()
    return redirect("/")


@APP.route('/plugins')
def plugins():
    return render_template('default/plugins.html')

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
