from abc import ABCMeta, abstractmethod
from typing import Any, Dict, List

from ..dataloader import DataLoader


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
    def write_loader(
        self,
        dataloader: DataLoader,
        options: Dict[str, Any] = None,
    ) -> None:
        """
        Write the contents by data loader.
        Arguments:
            dataloader: The data loader to get item
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
