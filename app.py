from flask import Flask, render_template 
from routes import othello_bp

app = Flask(__name__)

app.register_blueprint(othello_bp, url_prefix="/othello")

if (__name__ == "__main__"):
    app.run(debug=True)
