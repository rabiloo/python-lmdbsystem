import os
import re
import warnings

from glob import glob
from typing import Any, Dict, Generator, List, Optional, Tuple

from lmdbsystem.dataloader import DataLoader
from lmdbsystem.utils import (
    csv_line_reader,
    dump_pickle,
    get_md5_file,
    get_relative_path,
    json_reader,
    normalize_path,
    raw_reader,
    removesuffix_path,
    str2bytes,
    text_line_reader,
    text_reader,
)


class ImageLoader(DataLoader):
    def __init__(
        self,
        directory: str,
        suffix: str,
        fn_md5_mode: str,
        fn_md5_path: str,
    ):
        self.directory = directory
        self.suffix = suffix
        self.fn_md5_mode = fn_md5_mode
        self.fn_md5_path = fn_md5_path
        if fn_md5_mode == "r":
            self.dict_filename_md5 = json_reader(fn_md5_path)
        elif fn_md5_mode == "w":
            self.dict_filename_md5 = {}
        else:
            raise ValueError(f"Don't support fn_md5_mode: {fn_md5_mode}")
        self.file_paths = sorted(glob(f"{directory}/**/*{suffix}", recursive=True))

    def iterator(self) -> Generator[Tuple[Optional[bytes], Optional[bytes]], Any, None]:
        for file_path in self.file_paths:
            yield self[file_path]

    def __getitem__(self, file_path: str) -> Tuple[Optional[bytes], Optional[bytes]]:
        filename = get_relative_path(self.directory, file_path).removesuffix(self.suffix)
        value = raw_reader(file_path)
        if self.fn_md5_mode == "r":
            md5_file = self.dict_filename_md5[filename]
            value = dump_pickle((str2bytes(get_md5_file(file_path)), value))
        else:
            md5_file = get_md5_file(file_path)
            self.dict_filename_md5[filename] = md5_file
        key = str2bytes(md5_file)

        return key, value


class FaceppLoader(DataLoader):
    def __init__(
        self, directory: str, suffix: str, fn_md5_path: str, keys_extracted: List[str], values_map: Dict[str, str]
    ):
        self.directory = directory
        self.suffix = suffix
        self.keys_extracted = keys_extracted
        self.values_map = values_map
        self.dict_filename_md5 = json_reader(fn_md5_path)
        self.file_paths = sorted(glob(f"{directory}/**/*{suffix}", recursive=True))

    def iterator(self) -> Generator[Tuple[Optional[bytes], Optional[bytes]], Any, None]:
        for file_path in self.file_paths:
            yield self[file_path]

    def __getitem__(self, file_path: str) -> Tuple[Optional[bytes], Optional[bytes]]:
        md5_file = self.dict_filename_md5[get_relative_path(self.directory, file_path).removesuffix(self.suffix)]
        key = str2bytes(md5_file)
        sub_key = str2bytes(get_md5_file(file_path))

        data = json_reader(file_path)
        if data["face_num"] == 0:
            return None, None

        attribute = data["faces"][0]["attributes"]
        for _key in self.keys_extracted:
            attribute = attribute[_key]

        if self.values_map:
            attribute = self.values_map.get(attribute, attribute)

        value = dump_pickle((sub_key, str2bytes(str(attribute))))
        return key, value


class BaiduLoader(DataLoader):
    def __init__(
        self,
        directory: str,
        suffix: str,
        fn_md5_path: str,
        keys_extracted: List[str],
        key_probability: Optional[float],
        values_map: Optional[Dict[str, str]],
    ):
        self.directory = directory
        self.suffix = suffix
        self.keys_extracted = keys_extracted
        self.key_probability = key_probability
        self.values_map = values_map
        self.dict_filename_md5 = json_reader(fn_md5_path)
        self.file_paths = sorted(glob(f"{directory}/**/*{suffix}", recursive=True))

    def iterator(self) -> Generator[Tuple[Optional[bytes], Optional[bytes]], Any, None]:
        for file_path in self.file_paths:
            yield self[file_path]

    def __getitem__(self, file_path: str) -> Tuple[Optional[bytes], Optional[bytes]]:
        md5_file = self.dict_filename_md5[get_relative_path(self.directory, file_path).removesuffix(self.suffix)]
        key = str2bytes(md5_file)
        sub_key = str2bytes(get_md5_file(file_path))

        data = json_reader(file_path)
        if data["face_num"] == 0:
            return None, None

        attribute = data["face_list"][0]
        for _key in self.keys_extracted:
            if "probability" in attribute and attribute["probability"] < self.key_probability:
                attribute = None
                break
            attribute = attribute[_key]

        if attribute is None:
            return None, None

        if self.values_map:
            attribute = self.values_map.get(attribute, attribute)

        value = dump_pickle((sub_key, str2bytes(str(attribute))))
        return key, value


class VisageLoader(DataLoader):
    def __init__(
        self, directory: str, suffix: str, fn_md5_path: str, keys_extracted: List[str], values_map: Dict[str, str]
    ):
        self.directory = directory
        self.suffix = suffix
        self.keys_extracted = keys_extracted
        self.values_map = values_map
        self.dict_filename_md5 = json_reader(fn_md5_path)
        self.file_paths = sorted(glob(f"{directory}/**/*{suffix}", recursive=True))

    def iterator(self) -> Generator[Tuple[Optional[bytes], Optional[bytes]], Any, None]:
        for file_path in self.file_paths:
            yield self[file_path]

    def __getitem__(self, file_path: str) -> Tuple[Optional[bytes], Optional[bytes]]:
        md5_file = self.dict_filename_md5[get_relative_path(self.directory, file_path).removesuffix(self.suffix)]
        key = str2bytes(md5_file)
        sub_key = str2bytes(get_md5_file(file_path))

        data = json_reader(file_path)
        if not data:
            return None, None

        attribute = data[self.keys_extracted[0]]

        if self.values_map:
            attribute = self.values_map.get(attribute, attribute)

        value = dump_pickle((sub_key, str2bytes(str(attribute))))
        return key, value


class LabelInFilenameLoader(DataLoader):
    def __init__(
        self,
        directory: str,
        suffix: str,
        fn_md5_path: str,
        values_index: List[int],
        values_map: Dict[str, str],
        delimiter: str,
    ):
        self.directory = directory
        self.suffix = suffix
        self.values_map = values_map
        self.delimiter = delimiter
        self.values_index = values_index
        self.dict_filename_md5 = json_reader(fn_md5_path)
        self.file_paths = sorted(glob(f"{directory}/**/*{suffix}", recursive=True))

    def iterator(self) -> Generator[Tuple[Optional[bytes], Optional[bytes]], Any, None]:
        for file_path in self.file_paths:
            yield self[file_path]

    def __getitem__(self, file_path: str) -> Tuple[Optional[bytes], Optional[bytes]]:
        md5_file = self.dict_filename_md5[get_relative_path(self.directory, file_path).removesuffix(self.suffix)]
        key = str2bytes(md5_file)
        sub_key = str2bytes(get_md5_file(file_path))

        line_values = os.path.basename(file_path).removesuffix(self.suffix).split(self.delimiter)
        labels = [value.strip() for index, value in enumerate(line_values) if index in self.values_index]

        if self.values_map:
            if "type" in self.values_map:
                value_type = self.values_map["type"]
                labels = [str(eval(value_type)(item)) for item in labels]
            else:
                labels = [self.values_map.get(item, item) for item in labels]

        value = dump_pickle((sub_key, str2bytes(" ".join(labels))))
        return key, value


class LabelInTxtLoader(DataLoader):
    def __init__(
        self,
        directory: str,
        suffix: str,
        fn_md5_path: str,
        values_index: List[int],
        values_map: Dict[str, str],
        delimiter: str,
    ):
        self.directory = directory
        self.suffix = suffix
        self.values_map = values_map
        self.delimiter = delimiter
        self.values_index = values_index
        self.dict_filename_md5 = json_reader(fn_md5_path)
        self.file_paths = sorted(glob(f"{directory}/**/*{suffix}", recursive=True))

    def iterator(self) -> Generator[Tuple[Optional[bytes], Optional[bytes]], Any, None]:
        for file_path in self.file_paths:
            yield self[file_path]

    def __getitem__(self, file_path: str) -> Tuple[Optional[bytes], Optional[bytes]]:
        md5_file = self.dict_filename_md5[get_relative_path(self.directory, file_path).removesuffix(self.suffix)]
        key = str2bytes(md5_file)
        sub_key = str2bytes(get_md5_file(file_path))

        line_values = text_reader(file_path).split(self.delimiter)
        labels = [value.strip() for index, value in enumerate(line_values) if index in self.values_index]

        if self.values_map:
            if "type" in self.values_map:
                value_type = self.values_map["type"]
                labels = [str(eval(value_type)(item)) for item in labels]
            else:
                labels = [self.values_map.get(item, item) for item in labels]

        value = dump_pickle((sub_key, str2bytes(" ".join(labels))))
        return key, value


class LabelInSomeCsvLoader(DataLoader):
    def __init__(
        self,
        file_paths: str,
        fn_md5_path: str,
        key_index: int,
        values_index: List[int],
        values_map: Dict[str, str],
        delimiter: str,
        skip_header: bool = False,
    ):
        self.file_paths = file_paths
        self.key_index = key_index
        self.values_index = values_index
        self.values_map = values_map
        self.delimiter = delimiter
        self.skip_header = skip_header
        self.dict_filename_md5 = json_reader(fn_md5_path)

    def iterator(self) -> Generator[Tuple[Optional[bytes], Optional[bytes]], Any, None]:
        for file_path in self.file_paths:
            sub_key = str2bytes(get_md5_file(file_path))
            for line_values in csv_line_reader(file_path, self.delimiter, self.skip_header):
                yield self[(sub_key, line_values)]

    def __getitem__(self, item: Any) -> Tuple[Optional[bytes], Optional[bytes]]:
        sub_key, line_values = item
        filename = removesuffix_path(normalize_path(line_values[self.key_index]))
        if filename not in self.dict_filename_md5:
            warnings.warn(f"File {filename} not in image folder")
            return None, None
        md5_file = self.dict_filename_md5[filename]
        key = str2bytes(md5_file)

        labels = [value.strip() for index, value in enumerate(line_values) if index in self.values_index]

        if self.values_map:
            if "type" in self.values_map:
                value_type = self.values_map["type"]
                labels = [str(eval(value_type)(item)) for item in labels]
            else:
                labels = [self.values_map.get(item, item) for item in labels]

        value = dump_pickle((sub_key, str2bytes(" ".join(labels))))
        return key, value


class LabelInSomeTxtLoader(DataLoader):
    def __init__(
        self,
        file_paths: str,
        fn_md5_path: str,
        key_index: int,
        values_index: List[int],
        values_map: Dict[str, str],
        delimiter: str,
    ):
        self.file_paths = file_paths
        self.key_index = key_index
        self.values_index = values_index
        self.values_map = values_map
        self.delimiter = delimiter
        self.dict_filename_md5 = json_reader(fn_md5_path)

    def iterator(self) -> Generator[Tuple[Optional[bytes], Optional[bytes]], Any, None]:
        for file_path in self.file_paths:
            sub_key = str2bytes(get_md5_file(file_path))
            for line in text_line_reader(file_path):
                yield self[(sub_key, line)]

    def __getitem__(self, item: Any) -> Tuple[Optional[bytes], Optional[bytes]]:
        sub_key, line = item
        line_values = line.split(self.delimiter)

        filename = removesuffix_path(normalize_path(line_values[self.key_index]))
        if filename not in self.dict_filename_md5:
            warnings.warn(f"File {filename} not in image folder")
            return None, None
        md5_file = self.dict_filename_md5[filename]
        key = str2bytes(md5_file)

        labels = [value.strip() for index, value in enumerate(line_values) if index in self.values_index]

        if self.values_map:
            if "type" in self.values_map:
                value_type = self.values_map["type"]
                labels = [str(eval(value_type)(item)) for item in labels]
            else:
                labels = [self.values_map.get(item, item) for item in labels]

        value = dump_pickle((sub_key, str2bytes(" ".join(labels))))
        return key, value


class LabelInKeyInSomeTxtLoader(DataLoader):
    def __init__(
        self,
        file_paths: str,
        fn_md5_path: str,
        key_index: int,
        pattern_value_in_key: str,
        type_value_in_key: str,
        values_map: Dict[str, str],
        delimiter: str,
    ):
        self.file_paths = file_paths
        self.key_index = key_index
        self.pattern = re.compile(pattern_value_in_key)
        self.value_type_of_key = type_value_in_key
        self.values_map = values_map
        self.delimiter = delimiter
        self.dict_filename_md5 = json_reader(fn_md5_path)

    def iterator(self) -> Generator[Tuple[Optional[bytes], Optional[bytes]], Any, None]:
        for file_path in self.file_paths:
            sub_key = str2bytes(get_md5_file(file_path))
            for line in text_line_reader(file_path):
                yield self[(sub_key, line)]

    def __getitem__(self, item: Any) -> Tuple[Optional[bytes], Optional[bytes]]:
        sub_key, line = item
        line_values = line.split(self.delimiter)

        filename = removesuffix_path(normalize_path(line_values[self.key_index]))
        if filename not in self.dict_filename_md5:
            warnings.warn(f"File {filename} not in image folder")
            return None, None
        md5_file = self.dict_filename_md5[filename]
        key = str2bytes(md5_file)

        res = self.pattern.search(line_values[self.key_index])
        labels = [str(eval(self.value_type_of_key)(res.group(1)))]

        if self.values_map:
            labels = [self.values_map.get(item, item) for item in labels]

        value = dump_pickle((sub_key, str2bytes(" ".join(labels))))
        return key, value
