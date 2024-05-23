import os

from os.path import dirname, join

import cv2
import numpy as np
import pytest

from PIL import Image

from lmdbsystem.lmdb import Lmdb
from lmdbsystem.read_adapters.cv2_image import Cv2ImageReadAdapter
from lmdbsystem.read_adapters.pil_image import PilImageReadAdapter
from lmdbsystem.write_adapters.image import ImageWriteAdapter


@pytest.mark.parametrize(
    "lmdb_path,key,image_path,image_type",
    (
        ("/tmp/image.lmdb", 1, join(dirname(__file__), "resources/images/1.jpg"), "cv2"),
        ("/tmp/image.lmdb", 3, join(dirname(__file__), "resources/images/3.jpg"), "pil"),
    ),
)
def test_write_image(lmdb_path: str, key: int, image_path: str, image_type: str):
    is_write = False
    if not os.path.exists(lmdb_path):
        is_write = True
    lmdb_obj = Lmdb(ImageWriteAdapter(path=lmdb_path))
    image = cv2.imread(image_path) if image_type == "cv2" else Image.open(image_path)
    if is_write:
        lmdb_obj.write(keys=[key], values=[image])
    else:
        lmdb_obj.update(keys=[key], values=[image])


@pytest.mark.parametrize(
    "lmdb_path,key,image_path,image_type",
    (
        ("/tmp/image.lmdb", 1, join(dirname(__file__), "resources/images/1.jpg"), "cv2"),
        ("/tmp/image.lmdb", 3, join(dirname(__file__), "resources/images/3.jpg"), "pil"),
    ),
)
def test_read_image(lmdb_path: str, key: int, image_path: str, image_type: str):
    if image_type == "cv2":
        obj = Lmdb(Cv2ImageReadAdapter(path=lmdb_path))
        img_expected = cv2.imread(image_path)
    else:
        obj = Lmdb(PilImageReadAdapter(path=lmdb_path))
        img_expected = Image.open(image_path)
    value = obj.read_key(str(key).encode("utf-8"))
    if image_type == "cv2":
        assert np.allclose(img_expected, value, atol=3)
    else:
        img_expected = np.asarray(img_expected, dtype=np.uint8)
        value = np.asarray(value, dtype=np.uint8)
        assert np.allclose(img_expected, value, atol=3)
