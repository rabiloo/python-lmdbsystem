import pickle

import lmdb

from data_helper.datatypes import bytes2str

from ..error import UnableToCloseFile, UnableToReadFile
from ..read_adapters import ReadAdapter


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

    def read_index(self, index: int) -> str:
        if index < 0 or index >= self.length:
            raise UnableToReadFile.with_location(self.path, f"Invalid index: {index}")

        key = self.keys[index]
        return self.read_key(key)

    def read_key(self, key: bytes) -> str:
        try:
            value = self.txn.get(key)
            try:
                contents = pickle.loads(value)
                _, label = contents
            except pickle.UnpicklingError:
                if isinstance(value, bytes):
                    label = value
                else:
                    label = bytes(value)
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
