from flask import Flask, render_template
from assobot.core.utils.logger import get_logger

LOGGER = get_logger(__name__)

app = Flask(__name__)

@app.route("/")
def home():
   return render_template('index.html')

def launch():
   LOGGER.info('START Assobot Application')
   app.run()
   LOGGER.info('Stop Assobot Application')