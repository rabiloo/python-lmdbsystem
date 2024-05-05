from abc import ABCMeta, abstractmethod


class ReadAdapter(metaclass=ABCMeta):
    """
    Read Adapter interface
    """

    @abstractmethod
    def read_index(self, index: int):
        """
        Read the contents of the lmdb file by index.
        Arguments:
            index: The index of data
        Returns:
            None
        """

    @abstractmethod
    def read_key(self, key: bytes):
        """
        Read the contents of the lmdb file by key.
        Arguments:
            key: The key of data
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
