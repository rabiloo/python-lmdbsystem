import pickle

from typing import Any, Dict, List, Union

import lmdb
import numpy as np
import numpy.typing as npt

from PIL.Image import Image
from tqdm import tqdm

from ..dataloader import DataLoader
from ..error import UnableToCloseFile, UnableToUpdateFile, UnableToWriteFile
from ..utils import cv22bytes, dump_pickle, json_writer, pil2bytes, str2bytes
from ..write_adapters import WriteAdapter


class ImageWriteAdapter(WriteAdapter):
    """
    Image Convertor adapter class
    """

    def __init__(
        self, path: str, map_size: int = 32212254720, readonly: bool = False, meminit: bool = False  # 30GB
    ) -> None:
        self.path = path
        self.db = lmdb.open(
            path, map_size=map_size, subdir=False, readonly=readonly, map_async=True, meminit=meminit, lock=False
        )

    def update(
        self,
        keys: List[Union[str, bytes]],
        values: List[Union[bytes, Image, npt.NDArray[np.uint8]]],
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
        if len(keys) != len(values):
            raise UnableToWriteFile.with_location(self.path, "Length of keys and values must match")

        write_frequency = options.get("write_frequency", 500)

        with self.db.begin(write=False, buffers=True) as txn:
            base_length = pickle.loads(txn.get(b"__len__"))
            base_keys = pickle.loads(txn.get(b"__keys__"))

        try:
            txn = self.db.begin(write=True)
            for idx, (key, value) in enumerate(tqdm(zip(keys, values)), start=1):
                if not isinstance(key, bytes):
                    key = str2bytes(str(key))

                if isinstance(value, np.ndarray):
                    value = cv22bytes(value)
                elif isinstance(value, Image):
                    value = pil2bytes(value)

                if not isinstance(value, bytes):
                    raise UnableToWriteFile.with_location(self.path, "Could not to supported value format")

                txn.put(key, value)
                if key not in base_keys:
                    base_keys.append(key)

                if write_frequency > 0 and idx % write_frequency == 0:
                    txn.commit()
                    txn = self.db.begin(write=True)

            txn.commit()
            if len(base_keys) > base_length:
                with self.db.begin(write=True) as txn:
                    txn.put(b"__keys__", dump_pickle(base_keys))
                    txn.put(b"__len__", dump_pickle(len(base_keys)))
        except Exception as ex:
            raise UnableToUpdateFile.with_location(self.path, str(ex))

    def write(
        self,
        keys: List[Union[str, bytes]],
        values: List[Union[bytes, Image, npt.NDArray[np.uint8]]],
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
        if len(keys) != len(values):
            raise UnableToWriteFile.with_location(self.path, "Length of keys and values must match")

        write_frequency = options.get("write_frequency", 500)

        try:
            txn = self.db.begin(write=True)
            keys_ = []
            for idx, (key, value) in enumerate(tqdm(zip(keys, values)), start=1):
                if not isinstance(key, bytes):
                    key = str2bytes(str(key))

                if isinstance(value, np.ndarray):
                    value = cv22bytes(value)
                elif isinstance(value, Image):
                    value = pil2bytes(value)

                if not isinstance(value, bytes):
                    raise UnableToWriteFile.with_location(self.path, "Could not to supported value format")

                txn.put(key, value)
                keys_.append(key)

                if write_frequency > 0 and idx % write_frequency == 0:
                    txn.commit()
                    txn = self.db.begin(write=True)

            # finish iterating through dataset
            txn.commit()
            with self.db.begin(write=True) as txn:
                txn.put(b"__keys__", dump_pickle(keys_))
                txn.put(b"__len__", dump_pickle(len(keys_)))

        except Exception as ex:
            raise UnableToWriteFile.with_location(self.path, str(ex))

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
        write_frequency = options.get("write_frequency", 500)
        try:
            txn = self.db.begin(write=True)
            keys = []
            for idx, (key, value) in enumerate(tqdm(dataloader.iterator()), start=1):
                if key is None or value is None:
                    continue

                txn.put(key, value)
                keys.append(key)

                if write_frequency > 0 and idx % write_frequency == 0:
                    txn.commit()
                    txn = self.db.begin(write=True)

            # finish iterating through dataset
            txn.commit()
            with self.db.begin(write=True) as txn:
                txn.put(b"__keys__", dump_pickle(keys))
                txn.put(b"__len__", dump_pickle(len(keys)))

            if dataloader.fn_md5_mode == "w":
                json_writer(dataloader.fn_md5_path, dataloader.dict_filename_md5)
        except Exception as ex:
            raise UnableToWriteFile.with_location(self.path, str(ex))

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
