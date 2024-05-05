import io
import pickle

import lmdb

from PIL import Image

from ..error import UnableToCloseFile, UnableToReadFile
from ..read_adapters import ReadAdapter


class PilImageReadAdapter(ReadAdapter):
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

    def read_index(self, index: int) -> Image.Image:
        try:
            key = self.keys[index]
            value = self.txn.get(key)
            try:
                contents = pickle.loads(value)
                _, image_byte = contents
            except pickle.UnpicklingError:
                image_byte = value

            with io.BytesIO() as buf:
                buf.write(image_byte)
                buf.seek(0)
                img = Image.open(buf).convert("RGB")
        except Exception as ex:
            raise UnableToReadFile.with_location(self.path, str(ex))

        return img

    def read_key(self, key: bytes) -> Image.Image:
        try:
            value = self.txn.get(key)
            try:
                contents = pickle.loads(value)
                _, image_byte = contents
            except pickle.UnpicklingError:
                image_byte = value

            with io.BytesIO() as buf:
                buf.write(image_byte)
                buf.seek(0)
                img = Image.open(buf).convert("RGB")
        except Exception as ex:
            raise UnableToReadFile.with_location(self.path, str(ex))

        return img

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
