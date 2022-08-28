from threading import Thread
from time import sleep, time
import config.judge as config

class TimedDict:
    def __init__(self, lifetime: int):
        self.__lifetime = lifetime
        self.__container = {}
        Thread(target=self.__reaper, daemon=True).start()

    def __contains__(self, obj):
        return obj in self.__container

    def __setitem__(self, key, val):
        if key in self.__container:
            raise ValueError(f'{val} already exists')

        self.__container[key] = (time(), val)

    def __getitem__(self, key):
        return self.__container[key][1]

    def __delitem__(self, key):
        del self.__container[key]

    def __reaper(self):
        while True:
            sleep(config.reaperTimeout)
            currentTime = time()
            toRemove = []
            for obj in self.__container:
                issueTime = self.__container[obj][0]
                if currentTime - issueTime > self.__lifetime:
                    toRemove.append(obj)
            for obj in toRemove:
                del self.__container[obj]
