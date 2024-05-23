from abc import ABCMeta, abstractmethod
from typing import Any, Generator, Optional, Tuple


class DataLoader(metaclass=ABCMeta):

    @abstractmethod
    def iterator(self) -> Generator[Tuple[Optional[bytes], Optional[bytes]], Any, None]:
        """
        Get item by yield from list items.
        Arguments:
        Returns:
            key: Any
            value: Any
        """

    @abstractmethod
    def __getitem__(self, index: Any) -> Tuple[Optional[bytes], Optional[bytes]]:
        """
        Get item by index.
        Arguments:
            index: Any
        Returns:
            key: Any
            value: Any
        """
