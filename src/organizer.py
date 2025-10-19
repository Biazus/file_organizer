from typing import List, Iterable, Optional, TypedDict
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
import logging

import os

logger = logging.getLogger(__name__)


class PathReader:
    def __init__(self, path):
        self.path = path


class FileInfo(TypedDict):
    path: str
    filename: str
    filesize: int
    filetype: str


class FileHandler:
    """
    Collect file info/metadata
    """
    def __init__(self):
        pass

    def retrieve_files_from_folder(self, folders: Iterable[Path], exclude_dirs: Iterable[Path] = ()) -> tuple[list[Path], list[Path]]:
        excluded = {Path(p).resolve() for p in exclude_dirs}
        directory_list: list[Path] = []
        file_list: list[Path] = []
        for folder in folders:
            for root, dirs, files in os.walk(
                folder,
                topdown=True,
                followlinks=False,
                onerror=lambda e: logger.warning("Walk error: %s", e),
            ):
                root_path = Path(root)
                dirs[:] = [d for d in dirs if (root_path / d).resolve() not in excluded]
                directory_list.append(root_path)
                for name in files:
                    file_list.append(root_path / name)
        logger.info("Found %d files in %d folders", len(file_list), len(directory_list))
        logger.debug("Directory list (first 100): %s", directory_list[:100])
        logger.debug("File list (first 100): %s", file_list[:100])
        return directory_list, file_list

    def as_dict(self, path: Path) -> Optional[FileInfo]:
        logger.debug("Reading %s", path)
        try:
            p = Path(path)
            if not p.is_file():
                return None
            st = p.stat()
            return FileInfo(**{
                "path": str(p),
                "filename": p.name,
                "filesize": st.st_size,
                "filetype": p.suffix.lower(),
            })
        except (FileNotFoundError, PermissionError, OSError) as e:
            logger.warning("Skipping %s (%s)", path, e)
            return None


class TaskManager:
    """ get files / folders, read them, build new structure"""
    def __init__(self, config):
        if config is None:
            logger.error("No config file")
            raise RuntimeError("No config found. Aborting")
        self.user_config = config
        self.directory_list: list[Path] = []
        self.file_list: list[Path] = []
        self.file_collection: list[FileInfo] = []
        self.tasks: list[Task] = []
        self.file_handler = FileHandler()

    def start(self):
        self.collect_all_objects()
        self.file_collection.clear()
        max_workers = min(64, (os.cpu_count() or 4) * 5)
        with ThreadPoolExecutor(max_workers=max_workers) as ex:
            self.file_collection.extend(
                info for info in ex.map(self.file_handler.as_dict, self.file_list) if info
            )

        # now we have the files and folders we can create the tasks to log, call llm, create structure proposal etc
        self.tasks.append(Task())  #Todo
        for task in self.tasks:
            task.run_thread()

    def collect_all_objects(self):
        logger.info("Collecting all objects from folders %s", self.user_config.folder.watch_folders)
        self.directory_list, self.file_list = self.file_handler.retrieve_files_from_folder(self.user_config.folder.watch_folders)

class Task:
    def __init__(self, *args, **kwargs):
        self.base_folder = kwargs.get("base_folder")

    def run_thread(self):
        pass