from queue import Queue
from threading import Thread, Lock
from traceback import format_exc


class ThreadPool:
    def __init__(self, size):
        self.size = size
        self.used = 0
        self.pending = Queue()
        self.lock = Lock()

    def addThread(self, func, args=(), kwargs={}):
        self.pending.put((func, args, kwargs))
        self.tryRun()

    def tryRun(self):
        self.lock.acquire()
        if self.used < self.size and not self.pending.empty():
            self.used += 1
            func, args, kwargs = self.pending.get()
            Thread(target=self.runner, args=(func, args, kwargs), daemon=True).start()
        self.lock.release()

    def runner(self, func, args, kwargs):
        try:
            func(*args, **kwargs)
        except:
            print(format_exc())

        self.lock.acquire()
        self.used -= 1
        self.lock.release()
        self.tryRun()
        