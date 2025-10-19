import logging
from config import UserConfig
from organizer import TaskManager


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    conf = UserConfig("config.yaml")
    TaskManager(conf).start()
