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
    value = Lmdb(TextReadAdapter(path=path)).read_index(index)
    assert value == expected


def test_update_text():
    # Not using mark.parametrize for this test
    list_keys = [
        [
            b"5cb730a83ab169468f9a7f37e8691dfb",
            b"5cb730a83ab169468f9a7f37e8691123",
            b"5cb730a83ab169468f9a7f37e86911456",
        ],
        [
            b"5cb730a83ab169468f9a7f37e8691789",
            b"5cb730a83ab169468f9a7f37e8691101",
            b"5cb730a83ab169468f9a7f37e8691102",
        ],
    ]
    list_values = [["2", "4", "5"], ["6", "7", "8"]]
    list_len = [4, 7]

    for i in range(2):
        lmdb_obj.update(keys=list_keys[i], values=list_values[i])
        reader_lmdb_obj = Lmdb(TextReadAdapter(path="/tmp/label.lmdb"))
        assert reader_lmdb_obj.read_key(list_keys[i][0]) == list_values[i][0]
        assert len(reader_lmdb_obj.adapter.keys) == list_len[i]
