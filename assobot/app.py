from crypt import methods
import os
from pathlib import *
import uuid
from assobot import TMP_FOLDER_PLUGIN
from flask import Flask, render_template, flash, redirect, request, url_for
from werkzeug.utils import secure_filename


from assobot.core.utils.logger import get_logger
from assobot.core.plugin.plugin_manager import PluginManager

LOGGER = get_logger(__name__)

app = Flask(__name__)

UPLOAD_FOLDER = os.path.dirname(os.path.realpath(__file__))
ALLOWED_EXTENSIONS = set(['zip'])

app = Flask(__name__)
manager = PluginManager()

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def upload_file():

   if request.method == 'POST':
      if 'file' not in request.files:
         flash('No file part')
         return redirect(request.url)
      file = request.files['file']

      if file.filename == '':
         flash('No selected file')
         return redirect(request.url)

      if file and allowed_file(file.filename):
         filename = secure_filename(file.filename)
         dst_file_path = Path(os.path.join(TMP_FOLDER_PLUGIN, filename))
         file.save(dst_file_path)
         manager.load_plugin(dst_file_path)

   return render_template('default/index.html', plugins=list(manager.plugins.values()))

@app.route('/plugin/<plugin_id>/settings')
def open_plugin_settings(plugin_id):
   plugin = manager.plugins.get(uuid.UUID(plugin_id), None)
   
   if plugin is None:
      return redirect('/')

   return render_template(f"plugins/{plugin.namespace}/settings.html")

@app.route('/plugin/<plugin_id>/remove')
def remove_plugin(plugin_id):
   plugin = manager.plugins.get(uuid.UUID(plugin_id), None)
   
   if plugin is None:
      redirect('/')

   manager.unload_plugin(plugin)

   return redirect('/')

@app.route('/plugin/<plugin_id>/enabled')
def enable_plugin(plugin_id):
   plugin = manager.plugins.get(uuid.UUID(plugin_id), None)
   
   if plugin is None:
      redirect('/')

   plugin.enabled = True

   return redirect('/')

@app.route('/plugin/<plugin_id>/disabled')
def disable_plugin(plugin_id):
   plugin = manager.plugins.get(uuid.UUID(plugin_id), None)
   
   if plugin is None:
      redirect('/')

   plugin.enabled = False

   return redirect('/')

def launch():
   LOGGER.info('START Assobot Application')
   app.run()
   LOGGER.info('STOP Assobot Application')