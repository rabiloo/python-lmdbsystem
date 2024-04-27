import pickle

import lmdb

from ..error import UnableToCloseFile, UnableToReadFile
from ..read_adapters import ReadAdapter
from ..utils import bytes2str


class TextReadAdapter(ReadAdapter):
    """
    PIL Image Convertor adapter class
    """

    def __init__(
        self, path: str, map_size: int = 32212254720, readonly: bool = True, meminit: bool = False  # 30GB
    ) -> None:
        self.path = path
        self.db = lmdb.open(
            path, map_size=map_size, subdir=False, readonly=readonly, readahead=False, meminit=meminit, lock=False
        )
        self.txn = self.db.begin(write=False, buffers=True)
        self.length = pickle.loads(self.txn.get(b"__len__"))
        self.keys = pickle.loads(self.txn.get(b"__keys__"))

    def read(self, index) -> str:
        try:
            key = self.keys[index]
            value = self.txn.get(key)
            try:
                contents = pickle.loads(value)
                _, label = contents
            except pickle.UnpicklingError:
                label = value

            label = bytes2str(label)
        except Exception as ex:
            raise UnableToReadFile.with_location(self.path, str(ex))

        return label

    def close(self) -> None:
        """
        Close the lmdb file
        Returns:
            None
        """
        try:
            self.db.sync()
            self.db.close()
        except TypeError as ex:
            raise UnableToCloseFile.with_location(self.path, str(ex))