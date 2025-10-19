import logging
import os
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer

from config import UserConfig
from data import FileInfo
from utils.file_readers import FileHandler

logger = logging.getLogger(__name__)


class WatcherManager:
    """
    Manages a watchdog observer to monitor a configured directory for file system changes.

    Initialized with a UserConfig, sets up a FileHandler and an Observer, and monitors the
    configured watch directory. Calling run() schedules the handler (non-recursive),
    starts the observer, and blocks until interrupted; on interruption, the observer is
    stopped and joined.
    Args:
        user_config (UserConfig): Loaded configuration containing folder paths.
    Notes:
        Currently monitors a single directory and prints status messages to stdout.

    """

    def __init__(self, user_config: UserConfig):
        self.directory = Path(user_config.folder.watch_folders)  # TODO multiple folders
        self.event_handler = FileHandler()
        self.observer = Observer()

    def run(self):
        print(f"Monitoring: {self.directory}")
        self.observer.schedule(self.event_handler, str(self.directory), recursive=False)
        self.observer.start()

        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\nEncerrando monitoramento...")
            self.observer.stop()

        self.observer.join()


class DryManager:
    """
    Manage discovery and metadata collection for configured watch folders.

    On start(), scans all watch_folders to populate directory_list and file_list,
    then builds file_collection by extracting FileInfo for each file concurrently.
    Concurrency uses a thread pool sized as min(64, (os.cpu_count() or 4) * 5).
    Progress and issues are logged via the module logger, and FileHandler performs
    traversal and file stat reads.

    Args:
        user_config (UserConfig): Configuration providing folder.watch_folders.

    """

    def __init__(self, user_config: UserConfig):
        self.watch_folders = user_config.folder.watch_folders
        self.directory_list: list[Path] = []
        self.file_list: list[Path] = []
        self.file_collection: list[FileInfo] = []
        # self.tasks: list[Task] = []
        self.file_handler = FileHandler()

    def start(self):
        self.collect_all_objects()
        self.file_collection.clear()
        max_workers = min(64, (os.cpu_count() or 4) * 5)
        with ThreadPoolExecutor(max_workers=max_workers) as ex:
            self.file_collection.extend(
                info
                for info in ex.map(self.file_handler.as_dict, self.file_list)
                if info
            )

        # now we have the files and folders we can create the tasks to log, call llm, create structure proposal etc
        # self.tasks.append(Task())  # Todo
        # for task in self.tasks:
        #    task.run_thread()

    def collect_all_objects(self):
        """
        Populate directory and file lists from the configured watch folders.

        The function logs the operation, walks all watch folders using FileHandler,
        and assigns `directory_list` and `file_list` accordingly.

        Returns:
        - None
        """
        logger.info("Collecting all objects from folders %s", self.watch_folders)
        self.directory_list, self.file_list = (
            self.file_handler.retrieve_files_from_folder(self.watch_folders)
        )
