from config import UserConfig
from organizer import TaskManager

if __name__ == "__main__":
    conf = UserConfig("config.yaml")
    TaskManager(conf).start()
    print(type(conf.behavior))
    print(type(conf.folder))
