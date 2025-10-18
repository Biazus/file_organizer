from config import UserConfig

if __name__ == "__main__":
    conf = UserConfig("config.yaml")
    print(conf.behavior.mode_default)
    print(conf.folder)
