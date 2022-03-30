from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def home():
   return render_template('index.html')

@app.route("/plugins")
def plugins():
   return render_template('home.html')

@app.route("/plugins/welcome-message")
def welcomeMessage():
   return render_template('/plugins/welcome_message.html')

def launch():
    app.run()