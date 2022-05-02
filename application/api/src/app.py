"""Flask Application"""

# load libaries
from flask import Flask, jsonify, session
import sys

# load modules
from endpoints.authentication import authentication_blueprint
from endpoints.motion import motion_blueprint
# init Flask app
app = Flask(__name__)
app.secret_key = "testing"
# register blueprints. ensure that all paths are versioned!
app.register_blueprint(authentication_blueprint, url_prefix="/api/auth")
app.register_blueprint(motion_blueprint, url_prefix="/api/motion")