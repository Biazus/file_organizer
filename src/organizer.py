from managers import DryManager, WatcherManager

import logging

logger = logging.getLogger(__name__)


class PathReader:
    def __init__(self, path):
        self.path = path



class TaskManager:
    """ get files / folders, read them, build new structure"""
    def __init__(self, config):
        if config is None:
            logger.error("No config file")
            raise RuntimeError("No config found. Aborting")
        self.user_config = config

        self.monitoring_system = self._get_monitoring_system()

    #factory
    def _get_monitoring_system(self):
        if self.user_config.behavior.mode_default == "dry":
            return DryManager
        elif self.user_config.behavior.mode_default == "active":
            return WatcherManager

    def start(self):
        self.monitoring_system(self.user_config).start()

class Task:
    def __init__(self, *args, **kwargs):
        self.base_folder = kwargs.get("base_folder")

    def run_thread(self):
        pass

