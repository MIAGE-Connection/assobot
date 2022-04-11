import json
import uuid
from pathlib import Path

from assobot import APP, AUTH_MANAGER
from flask import *
from werkzeug.utils import secure_filename

def get_auth_context():
   return AUTH_MANAGER.get(session['token'])

@APP.route('/guilds/<guild_id>/plugins/<plugin_id>', methods=['GET', 'POST'])
def plugin_settings_open(guild_id, plugin_id):
   ctx = get_auth_context()
   plugin = ctx.guild.plugins.get(uuid.UUID(plugin_id), None)
   
   if plugin is None:
      return redirect(f'/guilds/{guild_id}')

   if request.method == 'POST':
      data = request.form.to_dict(flat=False)
      plugin.get_settings_manager().update(data)

   return render_template(f"plugins/{plugin.namespace}/settings.html", plugin=plugin)

@APP.route('/guilds/<guild_id>/plugins/<plugin_id>/enabled', methods=['GET'])
def plugin_enabled(guild_id, plugin_id):
   ctx = get_auth_context()
   plugin = ctx.guild.plugins.get(uuid.UUID(plugin_id), None)
   
   if plugin is None:
      return redirect(f'/guilds/{guild_id}')

   plugin.get_settings_manager().set("enabled", True)

   return json.dumps({'success':True}), 200, {'ContentType':'application/json'} 

@APP.route('/guilds/<guild_id>/plugins/<plugin_id>/disabled', methods=['GET'])
def plugin_disabled(guild_id, plugin_id):
   ctx = get_auth_context()
   plugin = ctx.guild.plugins.get(uuid.UUID(plugin_id), None)
   
   if plugin is None:
      return redirect(f'/guilds/{guild_id}')

   plugin.get_settings_manager().set("enabled", False)

   return json.dumps({'success':True}), 200, {'ContentType':'application/json'} 

@APP.route('/guilds/<guild_id>/plugins/<plugin_id>/uninstall', methods=['GET', 'POST'])
def plugin_uninstall(guild_id, plugin_id):
   ctx = get_auth_context()
   plugin = ctx.guild.plugins.get(uuid.UUID(plugin_id), None)
   
   if plugin is None:
      return redirect(f'/guilds/{guild_id}')

   ctx.guild.remove_plugin(plugin)

   return redirect(f'/guilds/{guild_id}')
