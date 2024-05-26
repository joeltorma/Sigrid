import atexit
import concurrent.futures
import timer
#Thread manager class
class ThreadManager:
    def __init__(self):
        self.thread_pool = concurrent.futures.ThreadPoolExecutor(max_workers=5)
        self.active_threads = {}
        atexit.register(self.shutdown)
    
    def submit_task(self, target_time):
        if target_time not in self.active_threads:
            thread = timer.TimeActionThread(target_time)
            self.active_threads[target_time] = self.thread_pool.submit(thread.run)
    
    def close_task(self, target_time):
        if target_time not in self.active_threads:
            future = self.active_threads.pop(target_time)
            future.cancel()
            
    def shutdown(self):
        # Implement the shutdown logic here
        print("Shutting down ThreadManager...")
        self.thread_pool.shutdown(wait=False)