import warnings

from typing import Any, Dict, List

import lmdb

from tqdm import tqdm

from ..error import UnableToCloseFile, UnableToWriteFile
from ..utils import (
    csv_line_reader,
    dump_pickle,
    get_md5_file,
    json_reader,
    normalize_path,
    removesuffix_path,
    str2bytes,
)
from ..write_adapters import WriteAdapter


class CsvWriteAdapter(WriteAdapter):
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
        if fn_md5_mode == "r":
            dict_filename_md5 = json_reader(fn_md5_path)
        else:
            raise ValueError(f"Don't support fn_md5_mode: {fn_md5_mode}")

        key_index = options.get("key_index")
        values_index = options.get("values_index")
        values_map = options.get("values_map")
        delimiter = options.get("delimiter")
        skip_header = options.get("skip_header", False)
        write_frequency = options.get("write_frequency", 500)

        try:
            txn = self.db.begin(write=True)
            keys = []
            for file_path in file_paths:
                sub_key = str2bytes(get_md5_file(file_path))

                for idx, line_values in tqdm(enumerate(csv_line_reader(file_path, delimiter, skip_header))):
                    filename = removesuffix_path(normalize_path(line_values[key_index]))
                    if filename not in dict_filename_md5:
                        warnings.warn(f"File {filename} not in image folder")
                        continue
                    md5_file = dict_filename_md5[filename]
                    key = str2bytes(md5_file)

                    labels = [value.strip() for index, value in enumerate(line_values) if index in values_index]

                    if values_map:
                        labels = [values_map.get(item, item) for item in labels]

                    value = dump_pickle((sub_key, str2bytes(" ".join(labels))))

                    txn.put(key, value)
                    keys.append(key)

                    if write_frequency > 0 and idx % write_frequency == 0:
                        txn.commit()
                        txn = self.db.begin(write=True)

                txn.commit()
                txn = self.db.begin(write=True)

            # finish iterating through dataset
            txn.commit()
            with self.db.begin(write=True) as txn:
                txn.put(b"__keys__", dump_pickle(keys))
                txn.put(b"__len__", dump_pickle(len(keys)))

        except Exception as ex:
            raise UnableToWriteFile.with_location(self.path, str(ex))

    def write_dir(
        self, directory: str, suffix: str, fn_md5_mode: str, fn_md5_path: str, options: Dict[str, Any] = None
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
        raise NotImplementedError

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
