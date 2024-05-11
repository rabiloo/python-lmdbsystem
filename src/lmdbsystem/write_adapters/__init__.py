from abc import ABCMeta, abstractmethod
from typing import Any, Dict, List


class WriteAdapter(metaclass=ABCMeta):
    """
    Convertor interface
    """

    @abstractmethod
    def update(
        self,
        keys: List[str],
        values: List[str],
        options: Dict[str, Any] = None,
    ) -> None:
        """
        Update the contents of list keys and values to the lmdb.
        Arguments:
            keys: The list of keys
            values: The list of string
            options: Update options
        Returns:
            None
        """

    @abstractmethod
    def write(
        self,
        keys: List[str],
        values: List[str],
        options: Dict[str, Any] = None,
    ) -> None:
        """
        Write the contents of list keys and values to the lmdb.
        Arguments:
            keys: The list of keys
            values: The list of string
            options: Write options
        Returns:
            None
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
