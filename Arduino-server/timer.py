from concurrent.futures import CancelledError
import time
import threading
import asyncio
import arduino
import datetime
import atexit

class TimeActionThread(threading.Thread):
    def __init__(self, time):
        super().__init__()
        self.time = time
        self._stop_event = threading.Event()
        
    def run(self):
        try:
            while not self._stop_event.is_set():
                current_time = time.localtime(time.time())
                if (datetime.time(hour=current_time.tm_hour, minute=current_time.tm_min)) == self.time:
                    setCoffe()
                    self.stop()
        except CancelledError:
            print("Thread Cancelled")

    
    def stop(self):
        self._stop_event.set()

def setCoffe():
    try:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(arduino.connect_to_websocket("On"))
        return True
    except Exception as e:
        print(e)
        return False