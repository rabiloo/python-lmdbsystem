from os.path import dirname, join

import pytest

from lmdbsystem.lmdb import Lmdb
from lmdbsystem.read_adapters.text import TextReadAdapter
from lmdbsystem.write_adapters.text import TextWriteAdapter

lmdb_obj = Lmdb(TextWriteAdapter(path="/tmp/label.lmdb"))
lmdb_obj.write_files(
    file_paths=[join(dirname(__file__), "resources/label.txt")],
    fn_md5_mode="r",
    fn_md5_path="/tmp/fn_md5.json",
    options={
        "delimiter": " ",
        "key_index": 0,
        "values_index": [1],
    },
)


@pytest.mark.dependency(depends=["test_read_image"])
@pytest.mark.parametrize(
    "path,index,expected,error",
    (
        ("/tmp/label.lmdb", 0, "1", None),
        ("/tmp/label.lmdb", 1, "3", None),
    ),
)
def test_read_text(path: str, index: int, expected: str, error: Exception):
    value = Lmdb(TextReadAdapter(path=path)).read(index)
    assert value == expected
