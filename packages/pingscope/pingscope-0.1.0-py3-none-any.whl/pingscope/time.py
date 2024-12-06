import time

class Time:
  @classmethod
  def cycle_sleep(cls, elapsedTime, maxSleepTime = 1.0):
    time.sleep(maxSleepTime - min(elapsedTime, maxSleepTime))

class Stopwatch:
  def __init__(self):
    self.start()

  def start(self):
    self.__StartTime = time.perf_counter()
    self.__ElapsedTime = 0.0

  def stop(self):
    self.__ElapsedTime = time.perf_counter() - self.__StartTime

  @property
  def ElapsedTime(self):
    return self.__ElapsedTime
