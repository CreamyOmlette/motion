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

  def save_motion(self, name, flexion_levels):
    # if("email" not in session):
    #   return "not logged in"
    if(np.isnan(flexion_levels).any()):
      return "has a nan"
    if(self._motions.find_one({"email": 'test', "name": name})):
      return "name exists"
    self._motions.insert_one({"email": 'test', "name": name, 'flexion_levels': flexion_levels})
    return 0
  
  def get_motion(self, name):
    # if("email" not in session):
    #   return jsonify({"status-code": 1})
    traj = self._motions.find_one({"email": 'test', "name": name})['flexion_levels']
    return traj
  
  def get_motions(self):
    presets = self._motions.find({"email": 'test'})
    return presets