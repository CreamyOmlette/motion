from flask import Blueprint, jsonify, request, session
from services.motion_sevice import MotionService
import numpy as np

motion_blueprint = Blueprint(name="motion_blueprint", import_name=__name__)
motion_service = MotionService()

@motion_blueprint.route('/save', methods=['POST'])
def save_trajectory():
  data = request.get_json()
  trajectory_points = data["trajectory_points"]
  name = data["name"]
  res = motion_service.save_motion(name, trajectory_points)
  return jsonify({"status": res})

@motion_blueprint.route('/', methods=['GET'])
def get_trajectory():
  data = request.get_json()
  name = data["name"]
  res = motion_service.get_motion(name)
  return jsonify({"trajectory_points": res})
