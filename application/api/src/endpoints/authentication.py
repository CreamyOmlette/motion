from flask import Blueprint, jsonify, request, session
from services.user_service import UserService
# define the blueprint
authentication_blueprint = Blueprint(name="authentication_blueprint", import_name=__name__)
user_service = UserService()

# note: global variables can be accessed from view functions

# add view function to the blueprint
@authentication_blueprint.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data["email"]
    password = data["password"]
    res = user_service.login(email, password)
    if(res):
        return jsonify({"status-code": 1})
    return jsonify({"status-code": 0})

@authentication_blueprint.route('/register', methods=['GET', 'POST'])
def register_user():
    data = request.get_json()
    email = data["email"]
    password = data["password"]
    name = data["name"]
    res = user_service.register(name, password, email)
    if(res):
        return jsonify({"status-code": 1})
    return jsonify({"status-code": 0})

@authentication_blueprint.route('/login', methods=['GET'])
def is_logged_in():
    if("email" in session):
        return jsonify({'response': True})
    return jsonify({'response': False})

@authentication_blueprint.route('/logout', methods=['GET', 'POST'])
def logout():
    if("email" in session):
        session.pop("email")
        return jsonify({'response': 0})
    return jsonify({'response': 1})

