from glob import glob
from typing import Any, Dict, List

import lmdb

from tqdm import tqdm

from ..error import UnableToCloseFile, UnableToWriteFile
from ..utils import dump_pickle, get_md5_file, get_relative_path, json_reader, json_writer, raw_reader, str2bytes
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
        raise NotImplementedError

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
        raise NotImplementedError

    def write_files(
        self, file_paths: List[str], fn_md5_mode: str, fn_md5_path: str, options: Dict[str, Any] = None
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
        raise NotImplementedError

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
        write_frequency = options.get("write_frequency", 500)
        if fn_md5_mode == "r":
            dict_filename_md5 = json_reader(fn_md5_path)
        elif fn_md5_mode == "w":
            dict_filename_md5 = {}
        else:
            raise ValueError(f"Don't support fn_md5_mode: {fn_md5_mode}")
        try:
            txn = self.db.begin(write=True)
            file_paths = sorted(glob(f"{directory}/**/*{suffix}", recursive=True))
            print(f"Handling with {len(file_paths)} file")
            keys = []
            for idx, file_path in tqdm(enumerate(file_paths)):
                if fn_md5_mode == "r":
                    md5_file = dict_filename_md5[get_relative_path(directory, file_path).removesuffix(suffix)]
                    key = str2bytes(md5_file)
                    sub_key = str2bytes(get_md5_file(file_path))
                    value = dump_pickle((sub_key, raw_reader(file_path)))
                else:
                    md5_file = get_md5_file(file_path)
                    key = str2bytes(md5_file)
                    value = raw_reader(file_path)
                    dict_filename_md5[get_relative_path(directory, file_path).removesuffix(suffix)] = md5_file

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

            if fn_md5_mode == "w":
                json_writer(fn_md5_path, dict_filename_md5)

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
