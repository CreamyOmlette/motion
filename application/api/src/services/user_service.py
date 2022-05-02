import pymongo
import bcrypt
from pymongo.server_api import ServerApi
from flask import session

class UserService:
  _client: pymongo.MongoClient
  _db: pymongo.database.Database
  _server_api: ServerApi

  def __init__(self) -> None:
    self._client = pymongo.MongoClient("mongodb+srv://al1g18:i69103501@cluster0.ccrnx.mongodb.net/myFirstDatabase?retryWrites=true&w=majority", server_api=ServerApi('1'))
    self._db = self._client.get_database('motion_sleeve')
    self.records = self._db.records
    pass

  def register(self, username, password, email):
    if(self.records.find_one({'username': username})):
      return 1
    if(self.records.find_one({'email': email})):
      return 1
    hash = self.hash_pass(password)
    self.records.insert_one({'username': username,'password': hash,'email': email})
    return 0

  def hash_pass(self, password):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

  def compare_hash(self, a, b):
    return bcrypt.checkpw(a, b)

  def login(self, email, password):
    user = self.records.find_one({'email': email})
    res = self.compare_hash(password.encode('utf-8'), user['password'])
    if(res):
      session['email'] = email
      return 0
    return 1
