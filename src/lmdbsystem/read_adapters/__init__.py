from abc import ABCMeta, abstractmethod


class ReadAdapter(metaclass=ABCMeta):
    """
    Read Adapter interface
    """

    @abstractmethod
    def read(self, index: int):
        """
        Read the contents of the lmdb file.
        Arguments:
            index: The index of data
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
