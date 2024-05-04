import csv
import hashlib
import json
import os
import pickle

from typing import Any, Dict, List

import numpy as np
import numpy.typing as npt


def array2bytes(array: npt) -> bytes:
    """Convert a numpy array to bytes"""
    return array.tobytes()


def str2bytes(string: str, encoding: str = "utf-8") -> bytes:
    """Convert a string to bytes"""
    return string.encode(encoding)


def bytes2array(byte: bytes) -> npt:
    """Convert a byte stream into a numpy array"""
    return np.frombuffer(byte, dtype=np.uint64)


def bytes2str(byte: bytes) -> str:
    """Convert a byte stream into a string"""
    return byte.decode("utf-8")


def text_reader(path: str) -> str:
    with open(path, "r") as fread:
        return fread.read()


def text_line_reader(path: str) -> str:
    with open(path, "r") as fread:
        for line in fread:
            line = line.strip()
            if line:
                yield line


def raw_reader(path: str) -> bytes:
    with open(path, "rb") as f:
        bin_data = f.read()
    return bin_data


def csv_line_reader(path: str, delimiter: str, skip_header: bool) -> List[Any]:
    with open(path, "r") as f:
        reader = csv.reader(f, delimiter=delimiter)

        if skip_header:
            next(reader)

        for row in reader:
            yield row


def json_reader(path: str) -> Dict[str, Any]:
    with open(path, "r") as f:
        data = json.load(f)
    return data


def json_writer(path: str, data: Any) -> None:
    with open(path, "w") as f:
        json_string = json.dumps(data)
        f.write(json_string)


def get_md5_file(path):
    bin_data = raw_reader(path)
    return hashlib.md5(bin_data).hexdigest()


def dump_pickle(obj):
    """
    Serialize an object.

    Returns :
        The pickled representation of the object obj as a bytes object
    """
    return pickle.dumps(obj)


def get_relative_path(directory: str, file_path: str):
    file_name = os.path.relpath(file_path, directory)

    return file_name


def normalize_path(file_path: str):
    return os.path.normpath(file_path)


def removesuffix_path(file_path: str):
    return file_path.rsplit(".", 1)[0]
