"""Flask Application"""

# load libaries
from flask import Flask, jsonify, session
from flask_cors import CORS, cross_origin
import sys

# load modules
from endpoints.authentication import authentication_blueprint
from endpoints.motion import motion_blueprint
# init Flask app
app = Flask(__name__)
cors = CORS(app, resources={r"/api/*": {"origins": "http://localhost:3000"}})
app.config['CORS_HEADERS'] = 'Content-Type'
app.secret_key = "testing"
# register blueprints. ensure that all paths are versioned!
app.register_blueprint(authentication_blueprint, url_prefix="/api/auth")
app.register_blueprint(motion_blueprint, url_prefix="/api/motion")

@app.after_request
def apply_caching(response):
    response.headers["Access-Control-Allow-Credentials"] = 'true'
    return response