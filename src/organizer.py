import logging

from managers import DryManager, WatcherManager

logger = logging.getLogger(__name__)


class PathReader:
    def __init__(self, path):
        self.path = path


class TaskManager:
    """
    Coordinate file discovery/monitoring based on the provided configuration.
    Selects a manager class according to behavior.mode_default:
    - "dry" -> DryManager
    - "active" -> WatcherManager
    and delegates execution to the selected manager
    """

    def __init__(self, config):
        if config is None:
            logger.error("No config file")
            raise RuntimeError("No config found. Aborting")
        self.user_config = config
        self.monitoring_system = self._get_monitoring_system()

    def _get_monitoring_system(self):
        if self.user_config.behavior.mode_default == "active":
            return WatcherManager
        return DryManager

    def start(self):
        self.monitoring_system(self.user_config).start()


class Task:
    def __init__(self, *args, **kwargs):
        self.base_folder = kwargs.get("base_folder")

    def run_thread(self):
        pass
