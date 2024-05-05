from os.path import dirname, join

import cv2
import numpy as np
import pytest

from PIL import Image, ImageChops

from lmdbsystem.lmdb import Lmdb
from lmdbsystem.read_adapters.cv2_image import Cv2ImageReadAdapter
from lmdbsystem.read_adapters.pil_image import PilImageReadAdapter
from lmdbsystem.write_adapters.image import ImageWriteAdapter

lmdb_obj = Lmdb(ImageWriteAdapter(path="/tmp/image.lmdb"))
lmdb_obj.write_dir(
    directory=join(dirname(__file__), "resources"),
    suffix=".jpg",
    fn_md5_mode="w",
    fn_md5_path="/tmp/fn_md5.json",
)


@pytest.mark.parametrize(
    "path,index,expected,error",
    (
        ("/tmp/image.lmdb", 0, join(dirname(__file__), "resources/images/1.jpg"), None),
        ("/tmp/image.lmdb", 1, join(dirname(__file__), "resources/images/3.jpg"), None),
    ),
)
def test_read_image(path: str, index: int, expected: str, error: Exception):
    value = Lmdb(Cv2ImageReadAdapter(path=path)).read_index(index)
    img_expected = cv2.imread(expected)
    assert np.allclose(img_expected, value)

    value = Lmdb(PilImageReadAdapter(path=path)).read_index(index)
    img_expected = Image.open(expected)
    assert ImageChops.difference(img_expected, value).getbbox() is None
