import datetime
from flask import request, Flask, jsonify
from flask_socketio import SocketIO
from gevent import monkey
from flask_cors import CORS
import threading
import asyncio
import websockets
import arduino
import threadManager
import time
import database as db
app = Flask(__name__)
socketio = SocketIO(app)
CORS(app)
state = "Off"
thread_pool_manager = threadManager.ThreadManager()


@app.route('/toggleAlarm', methods=['POST'])
def onOff():
    data = request.get_json()
    hour = data.get('hour')
    minute = data.get('minute')
    # Assuming 'isOn' is a boolean, defaulting to False
    state = data.get('active', False)

    # find correct alarm and start it
    hour, minute = db.findAlarm(hour, minute, state)
    if hour or minute == -1:
        return jsonify({'error': 'error'}), 400
    # If a old alarm is set to be active
    if state:
        time = datetime.time(hour=hour, minute=minute)
        thread_pool_manager.submit_task(time)
        return jsonify({"Alarm state": state}), 200

    # If a active alarm is set to be deactived
    thread_pool_manager.close_task(time)
    return jsonify({"status": "success"}), 200


@app.route('/coffe/timer', methods=['POST'])
def setTimer():
    data = request.get_json()
    hour = int(data.get("hour", 0))
    minute = int(data.get("minute", 0))

    time = datetime.time(hour=hour, minute=minute)

    thread_pool_manager.submit_task(time)
    # Here I wanna start a thread that runs in the background
    return jsonify({"status": "succes"})


@app.route('/createAlarm', methods=['POST'])
def createAlarm():
    data = request.get_json()
    hour = data.get('hour')
    minute = data.get('minute')
    print("Create Alarm function called")
    print(type(hour))

    status = db.createAlarm(hour, minute)

    if status != "OK":
        return jsonify({'Error': status}), 400

    time = datetime.time(hour=hour, minute=minute)
    thread_pool_manager.submit_task(time)

    return jsonify({"Succes": "Alarm has been created"}), 200


@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username', 0)
    password = data.get('password', 0)

    if db.login(username, password) == 'OK':
        return jsonify({'Succes': "Login success"}), 200

    return jsonify({'Status': 'wrong password or username'}), 400


@app.route('/getAllAlarms', methods=['GET'])
def getAllAlarms():
    alarms = db.getAllAlarm()
    if alarms == Exception:
        return jsonify({"error": "Internel Server Error"}), 500
    return jsonify({"Alarms": alarms}), 200


@app.route('/checkActive', methods=['GET'])
def checkActive():
    active = db.getActiveAlarms()
    if active:
        return jsonify({'active': True})
    return jsonify({'active': False})


def run_flask():
    app.run(debug=False, host='0.0.0.0', port=5001)


if __name__ == '__main__':
    run_flask()
