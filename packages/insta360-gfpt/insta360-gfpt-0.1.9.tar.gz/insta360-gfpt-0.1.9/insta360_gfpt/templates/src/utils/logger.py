import time
from loguru import logger as lg
import os

t = time.strftime("%Y_%m_%d")
project="VB"

class Loggings:
    __instance = None
    current_dir = os.getcwd()
    parent_dir = os.path.dirname(current_dir)
    lg.add(f"{parent_dir}\\logs\\{project}\\log_{t}.log", rotation="00:00", encoding="utf-8", enqueue=True)

    def __new__(cls, *args, **kwargs):
        if not cls.__instance:
            cls.__instance = super(Loggings, cls).__new__(cls, *args, **kwargs)

        return cls.__instance

    def info(self, msg):
        return lg.info(msg)

    def debug(self, msg):
        return lg.debug(msg)

    def warning(self, msg):
        return lg.warning(msg)

    def error(self, msg):
        return lg.error(msg)


logger = Loggings()