from flask import Flask, render_template 
from routes import othello_bp
from flask_cors import CORS

app = Flask(__name__)

CORS(app)

app.register_blueprint(othello_bp, url_prefix="/othello")

if (__name__ == "__main__"):
    app.run(debug=True)
