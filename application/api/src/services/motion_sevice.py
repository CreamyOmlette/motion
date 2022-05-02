import pymongo
import bcrypt
from pymongo.server_api import ServerApi
from flask import jsonify, session
import numpy as np

class MotionService:
  _client: pymongo.MongoClient
  _db: pymongo.database.Database
  _motions: pymongo.database.Collection

  def __init__(self) -> None:
    self._client = pymongo.MongoClient("mongodb+srv://al1g18:i69103501@cluster0.ccrnx.mongodb.net/myFirstDatabase?retryWrites=true&w=majority", server_api=ServerApi('1'))
    self._db = self._client.get_database('motion_sleeve')
    self._motions = self._db.motions
    pass

  def save_motion(self, name, trajectory_points):
    if("email" not in session):
      return "not logged in"
    if(np.isnan(trajectory_points).any()):
      return "has a nan"
    if(self._motions.find_one({"email": session['email'], "name": name})):
      return "name exists"
    self._motions.insert_one({"email": session['email'], "name": name, 'trajectory_points': trajectory_points})
    return 0
  
  def get_motion(self, name):
    if("email" not in session):
      return jsonify({"status-code": 1})
    traj = self._motions.find_one({"email": session['email'], "name": name})['trajectory_points']
    return traj