"""
Module flysystem
"""

from abc import ABCMeta, abstractmethod
from typing import Any, Dict, List, Union

import numpy as np
import numpy.typing as npt

from PIL import Image

from .read_adapters import ReadAdapter
from .write_adapters import WriteAdapter


class LmdbReader(metaclass=ABCMeta):
    """
    This interface contains everything to read from and inspect a lmdb file.
    All methods containing are non-destructive.
    """

    @abstractmethod
    def read(self, path: str) -> Union[npt.NDArray[np.uint8], Image.Image, str]:
        """
        Get the contents of a file.
        Arguments:
            path: The file path
        Returns:
            The contents of file as string
        """

    @abstractmethod
    def close(self) -> None:
        """
        Close the lmdb file
        Returns:
            None
        """


class LmdbWriter(metaclass=ABCMeta):
    """
    This interface contains everything to write to a lmdb file.
    All methods containing are non-destructive.
    """

    @abstractmethod
    def write_files(
        self,
        file_paths: List[str],
        fn_md5_mode: str,
        fn_md5_path: str,
        options: Dict[str, Any] = None,
    ) -> None:
        """
        Write the contents of list file to the lmdb.
        Arguments:
            file_paths: The list of file path
            fn_md5_mode: The mode of handle with filename_to_md5 file. Only support ["r", "w"] mode
            fn_md5_path: The path of filename_to_md5 file
            options: Write options
        Returns:
            None
        """

    @abstractmethod
    def write_dir(
        self,
        directory: str,
        suffix: str,
        fn_md5_mode: str,
        fn_md5_path: str,
        options: Dict[str, Any] = None,
    ) -> None:
        """
        Write all contents of a directory to the lmdb.
        Arguments:
            directory: The directory path
            suffix: The suffix of file
            fn_md5_mode: The mode of handle with filename_to_md5 file. Only support ["r", "w"] mode
            fn_md5_path: The path of filename_to_md5 file
            options: Write options
        Returns:
            None
        """

    @abstractmethod
    def close(self) -> None:
        """
        Close the lmdb file
        Returns:
            None
        """


class LmdbOperator(LmdbReader, LmdbWriter, metaclass=ABCMeta):
    """
    This interface contains everything from LmdbReader and LmdbWriter
    """


class Lmdb(LmdbOperator):
    """
    Filesystem
    """

    def __init__(
        self,
        adapter: Union[ReadAdapter, WriteAdapter],
        config: Dict[str, Any] = None,
    ):
        self.adapter = adapter
        self.config = config

    def read(self, index: int) -> Union[npt.NDArray[np.uint8], Image.Image, str]:
        return self.adapter.read(index)

    def write_files(
        self, file_paths: List[str], fn_md5_mode: str, fn_md5_path: str, options: Dict[str, Any] = None
    ) -> None:
        self.adapter.write_files(file_paths, fn_md5_mode, fn_md5_path, (self.config or {}) | (options or {}))

    def write_dir(
        self,
        directory: str,
        suffix: str,
        fn_md5_mode: str,
        fn_md5_path: str,
        options: Dict[str, Any] = None,
    ) -> None:
        self.adapter.write_dir(directory, suffix, fn_md5_mode, fn_md5_path, (self.config or {}) | (options or {}))

    def close(self) -> None:
        self.adapter.close()
