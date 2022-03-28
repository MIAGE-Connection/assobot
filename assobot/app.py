from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def home():
   return "Hello World from AssoBot!"

@app.route("/plugins")
def plugins():
   return render_template('home.html')

def launch():
    app.run()