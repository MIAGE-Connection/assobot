from assobot import APP, BOT, BOT_SECRET, TMP_FOLDER_PLUGIN
from flask import *
from threading import Thread
from functools import partial
import os
from pathlib import *
import uuid
from werkzeug.utils import secure_filename
import discord

from assobot.core.utils.logger import get_logger
from assobot.core.plugin.plugin_manager import PluginManager

LOGGER = get_logger(__name__)

APP.config['SECRET_KEY'] = uuid.uuid4()

UPLOAD_FOLDER = os.path.dirname(os.path.realpath(__file__))
ALLOWED_EXTENSIONS = set(['zip'])

manager = PluginManager()

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@APP.route('/', methods=['GET', 'POST'])
def home():

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

def launch():
   LOGGER.info('START Assobot Application')
   partial_run = partial(APP.run, host="127.0.0.1", port=5000, debug=True, use_reloader=False)
   Thread(target=partial_run).start()
   BOT.run(BOT_SECRET)
   LOGGER.info('STOP Assobot Application')