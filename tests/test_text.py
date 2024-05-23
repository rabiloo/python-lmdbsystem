import os

import pytest

from lmdbsystem.lmdb import Lmdb
from lmdbsystem.read_adapters.text import TextReadAdapter
from lmdbsystem.write_adapters.text import TextWriteAdapter


@pytest.mark.parametrize(
    "lmdb_path,key,value",
    (
        ("/tmp/label.lmdb", "0", "1"),
        ("/tmp/label.lmdb", "1", "3"),
    ),
)
def test_write_text(lmdb_path: str, key: str, value: str):
    is_write = False
    if not os.path.exists(lmdb_path):
        is_write = True
    lmdb_obj = Lmdb(TextWriteAdapter(path=lmdb_path))
    if is_write:
        lmdb_obj.write(keys=[key], values=[value])
    else:
        lmdb_obj.update(keys=[key], values=[value])


@pytest.mark.parametrize(
    "lmdb_path,index,value",
    (
        ("/tmp/label.lmdb", 0, "1"),
        ("/tmp/label.lmdb", 1, "3"),
    ),
)
def test_read_text(lmdb_path: str, index: int, value: str):
    value_ = Lmdb(TextReadAdapter(path=lmdb_path)).read_index(index)
    assert value_ == value
