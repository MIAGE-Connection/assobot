import os
import json
import uuid
from pathlib import Path

from assobot import APP, AUTH_MANAGER, ASSOBOT_PLUGIN_TEMP_FOLDER, PLUGIN_FACTORY
from flask import *
from werkzeug.utils import secure_filename

def get_auth_context():
   return AUTH_MANAGER.get(session['token'])

@APP.route('/guilds/<guild_id>/plugins/<plugin_id>', methods=['GET', 'POST'])
def plugin_settings_open(guild_id, plugin_id):
   ctx = get_auth_context()
   plugin = ctx.guild.plugins.get(uuid.UUID(plugin_id), None)
   
   if plugin is None:
      return redirect(f'/{guild_id}')

   if request.method == 'POST':
      data = request.form.to_dict(flat=False)
      plugin.settings.update(data)

   return render_template(f"plugins/{plugin.namespace}/settings.html", plugin=plugin)