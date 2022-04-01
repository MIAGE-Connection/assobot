import os
import uuid
from pathlib import Path

from assobot import APP, TMP_FOLDER_PLUGIN
from assobot.core.plugin.plugin_manager import PluginManager
from flask import *
from werkzeug.utils import secure_filename

ALLOWED_EXTENSIONS = set(['zip'])

manager = PluginManager()

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@APP.route('/plugin/<plugin_id>/settings')
def plugin_settings_open(plugin_id):
   plugin = manager.plugins.get(uuid.UUID(plugin_id), None)
   
   if plugin is None:
      return redirect('/plugins')

   return render_template(f"plugins/{plugin.namespace}/settings.html", plugin=plugin)

@APP.route('/plugin/<plugin_id>/settings/update',  methods=['POST'])
def plugin_settings_update(plugin_id):
   plugin = manager.plugins.get(uuid.UUID(plugin_id), None)
      
   if plugin is None:
      return redirect('/')

   data = request.form.to_dict(flat=False)

   plugin.settings.update(data)

   return redirect(f'/plugin/{plugin.id}/settings')

@APP.route('/plugin/<plugin_id>/remove')
def plugin_remove(plugin_id):
   plugin = manager.plugins.get(uuid.UUID(plugin_id), None)
   
   if plugin is None:
      redirect('/plugins/manage')

   manager.unload_plugin(plugin)

   return redirect('/plugins/manage')

@APP.route('/plugin/<plugin_id>/enabled')
def plugin_enable(plugin_id):
   plugin = manager.plugins.get(uuid.UUID(plugin_id), None)
   
   if plugin is None:
      redirect('/')

   plugin.enabled = True

   return redirect('/')

@APP.route('/plugin/<plugin_id>/disabled')
def plugin_disable(plugin_id):
   plugin = manager.plugins.get(uuid.UUID(plugin_id), None)
   
   if plugin is None:
      redirect('/')

   plugin.enabled = False

   return redirect('/')

@APP.route('/plugins/manage', methods=['GET', 'POST'])
def plugin_manage():

   if request.method == 'POST':
      if 'file' not in request.files:
         return redirect('/plugins/manage')

      file = request.files['file']

      if file.filename == '':
         return redirect(request.url)

      if file and allowed_file(file.filename):
         filename = secure_filename(file.filename)
         dst_file_path = Path(os.path.join(TMP_FOLDER_PLUGIN, filename))
         file.save(dst_file_path)
         manager.load_plugin(dst_file_path)

   return render_template('default/plugin/plugin_manage.html', plugins=list(manager.plugins.values()))

@APP.route('/plugins')
def plugin_list():
    return render_template('default/plugin/plugin_list.html')
