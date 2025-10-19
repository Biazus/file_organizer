from typing import TypedDict


class FileInfo(TypedDict):
    path: str
    filename: str
    filesize: int
    filetype: str