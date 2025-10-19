import logging

import os
from typing import List

logger = logging.getLogger(__name__)


class PathReader:
    def __init__(self, path):
        self.path = path


class FileHandler:
    """
    Collect file info/metadata
    """
    def __init__(self):
        pass

    def retrieve_files_from_folder(self, folders):
        directory_list, file_list = [], []
        for folder in folders:
            for root, a, files in os.walk(folder):
                directory_list.append(root)
                for file in files:
                    file_list.append(os.path.join(root, file))
        logger.info(f"Found {len(file_list)} files in {len(directory_list)} folders")
        logger.info(f"Directory list: {directory_list}")
        logger.info(f"File list: {file_list}")
        return directory_list, file_list

    def as_dict(self, path) -> dict[str, str]:
        logger.info(f"Reading {path}...")
        info = {
            "filename": os.path.basename(path),
            "filesize": os.stat(path).st_size,
            "filetype": os.path.splitext(path)[1],
        }
        logger.info(f"File info: {info}")
        return info


class TaskManager:
    """ get files / folders, read them, build new structure"""
    user_config = None
    file_list: List = []
    directory_list: List[str] = []
    file_collection: List[dict] = []
    def __init__(self, config):
        if not config:
            logger.error("No config file")
            raise RuntimeError("No config found. Aborting")
        self.user_config = config
        self.tasks = []
        self.file_handler = FileHandler()

    def start(self):
        self.collect_all_objects()
        for file in self.file_list:
            self.file_collection.append({file: self.file_handler.as_dict(file)})

        # now we have the files and folders we can create the tasks to log, call llm, create structure proposal etc
        self.tasks.append(Task())  #Todo
        for task in self.tasks:
            task.run_thread()

    def collect_all_objects(self):
        logger.info(f"Collecting all objects from folders {self.user_config.folder.watch_folders}")
        self.directory_list, self.file_list = self.file_handler.retrieve_files_from_folder(self.user_config.folder.watch_folders)

class Task:
    def __init__(self, *args, **kwargs):
        self.base_folder = kwargs.get("base_folder")

    def run_thread(self):
        pass
