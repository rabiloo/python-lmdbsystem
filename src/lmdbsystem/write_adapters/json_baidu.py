from glob import glob
from typing import Any, Dict, List

import lmdb
from tqdm import tqdm

from ..error import UnableToCloseFile, UnableToWriteFile
from ..utils import dump_pickle, get_md5_file, str2bytes, json_reader, get_relative_path
from ..write_adapters import WriteAdapter


class JsonBaiduWriteAdapter(WriteAdapter):
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

    def write_files(
        self,
        file_paths: List[str],
        fn_md5_mode: str,
        fn_md5_path: str,
        options: Dict[str, Any] = None
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
        if fn_md5_mode == "r":
            dict_filename_md5 = json_reader(fn_md5_path)
        else:
            raise ValueError(f"Don't support fn_md5_mode: {fn_md5_mode}")

        keys_extracted = options.get("keys_extracted")
        key_probability = options.get("key_probability")
        values_map = options.get("values_map")
        write_frequency = options.get("write_frequency", 500)

        try:
            txn = self.db.begin(write=True)
            file_paths = sorted(glob(f"{directory}/**/*{suffix}", recursive=True))
            keys = []
            for idx, file_path in tqdm(enumerate(file_paths)):
                md5_file = dict_filename_md5[get_relative_path(directory, file_path).removesuffix(suffix)]
                key = str2bytes(md5_file)
                sub_key = str2bytes(get_md5_file(file_path))

                data = json_reader(file_path)
                if data["face_num"] == 0:
                    continue

                attribute = data["face_list"][0]
                for _key in keys_extracted:
                    if "probability" in attribute and attribute["probability"] < key_probability:
                        attribute = None
                        break
                    attribute = attribute[_key]
                if attribute is None:
                    continue

                if values_map:
                    attribute = values_map.get(attribute, attribute)
                value = dump_pickle((sub_key, str2bytes(str(attribute))))

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
