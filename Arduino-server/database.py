from flask import jsonify
from pymongo import ReturnDocument
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import json

connectionString = 'mongodb+srv://isakolofaxelsson:LN5obMliukgWgUd1@smarthome.4dvbmcv.mongodb.net/?retryWrites=true&w=majority&appName=SmartHome'
client = MongoClient(connectionString)

def login(username, password):
    try:
        collection = client.get_database('SmartHome').get_collection('User')
        user = collection.find_one({'Username' : username})
        if user['password'] == password:
            return 'OK'
    
        
    except Exception as e:
        return e
    
    return jsonify({"Bad request": "Failed login"})  
    

def getAllAlarm():
    try:
        collection = client.get_database('SmartHome').get_collection('Alarms')
        alarms = collection.find({}, {'_id': 0})
        return list(alarms)
    except Exception as e:
        return e

def createAlarm(hour, minute):
    try:
        collection = client.get_database('SmartHome').get_collection('Alarms')
        collection.insert_one({'hour': hour, 'minute': minute, 'active': True})
        return "OK"
    except Exception as e:
        return e

def findAlarm(hour, minute, state):
    try:
        print(type(hour), type(minute), type(state))
        collection = client.get_database('SmartHome').get_collection('Alarms')
        update = {'$set': {'active':state }}
        alarm = collection.find_one_and_update(
            {'hour': hour, 'minute': minute},
              update=update,
              projection={'_id':0, 'active':0},
              return_document=ReturnDocument.AFTER)
              
        #check if alarm exist
        if alarm == None:
            return -1, -1
        
    except Exception as e:
        return -1, -1
    
    return alarm['hour'], alarm['minute']

def getActiveAlarms():
    try:
        collection = client.get_database("SmartHome").get_collection('Alarms')
        alarm = collection.find_one({'active': True}) 
        return alarm
    except Exception as e:
        return e