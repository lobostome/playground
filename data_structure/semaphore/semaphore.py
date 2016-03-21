import threading

class Semaphore(object):
    def __init__(self, value = 1):
        self.__cond = threading.Condition(threading.Lock())
        self.__value = value

    def acquire(self):
        rc = False
        self.__cond.acquire()
        while self.__value == 0:
            self.__cond.wait()
        else:
            self.__value = self.__value - 1
            rc = True
        self.__cond.release()
        return rc

    def release(self):
        self.__cond.acquire()
        self.__value = self.__value + 1
        self.__cond.notify()
        self.__cond.release()
