import logging
import os
from pathlib import Path
from typing import Iterable, List, Optional, TypedDict

import yaml

from data import FileInfo

logger = logging.getLogger(__name__)


class YamlReader:
    """
    Reads a YAML document from disk on initialization using yaml.safe_load.
    Args:
        path (str): Filesystem path to the YAML file to load.
    """

    data: dict = None

    def __init__(self, path: str):
        with open(path, "r") as file:
            try:
                self.data = yaml.safe_load(file)
            except yaml.YAMLError as exc:
                print("Error loading your file")


class FileHandler:
    """
    Collect and summarize basic filesystem metadata.

    This handler:
    - Recursively walks one or more folders, optionally excluding specific
      directories, and returns the discovered directories and files.
    - Converts a Path to a FileInfo record with path, filename, filesize, and
      filetype (lowercased suffix).
    """

    def __init__(self):
        pass

    def retrieve_files_from_folder(
        self, folders: Iterable[Path], exclude_dirs: Iterable[Path] = ()
    ) -> tuple[list[Path], list[Path]]:
        """
        Walk folders, skipping excluded dirs. Returns (directories, files) as lists of Path. Logs traversal errors and a brief summary.
        :param folders:
        :param exclude_dirs:
        :return:
        """
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
        logger.info("Directory list (first 50): %s", directory_list[:50])
        logger.info("File list (first 50): %s", file_list[:50])
        return directory_list, file_list

    def as_dict(self, path: Path) -> Optional[FileInfo]:
        logger.debug("Reading %s", path)
        try:
            p = Path(path)
            if not p.is_file():
                return None
            st = p.stat()
            return FileInfo(
                **{
                    "path": str(p),
                    "filename": p.name,
                    "filesize": st.st_size,
                    "filetype": p.suffix.lower(),
                }
            )
        except (FileNotFoundError, PermissionError, OSError) as e:
            logger.warning("Skipping %s (%s)", path, e)
            return None
