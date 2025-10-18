import os
from typing import List

class PathReader:
    def __init__(self, path):
        self.path = path


class FileReader:
    """
    Collect file info/metadata
    """
    def __init__(self, path):
        self.path = path
        self.file_info = os.stat(path)

    def as_dict(self) -> dict[str, str]:
        return {
            "filename": os.path.basename(self.path),
            "filesize": self.file_info.st_size,
            "filetype": os.path.splitext(self.path)[1],
        }


class TaskManager:
    """ get files / folders, read them, build new structure"""
    user_config = None
    file_list: List = []
    directory_list: List[str] = []
    def __init__(self, config):
        if not config:
            raise RuntimeError("No config found. Aborting")
        self.user_config = config
        self.tasks = []

    def start(self):
        self.collect_all_files()
        for file in self.file_list:
            print(FileReader(file).as_dict())
        self.tasks.append(Task())  #Todo
        for task in self.tasks:
            task.run_thread()

    def collect_all_files(self):
        for folder in self.user_config.folder.watch_folders:
            for root, a, files in os.walk(folder):
                self.directory_list.append(root)
                for file in files:
                    self.file_list.append(os.path.join(root, file))

class Task:
    def __init__(self, *args, **kwargs):
        self.base_folder = kwargs.get("base_folder")

    def run_thread(self):
        pass
