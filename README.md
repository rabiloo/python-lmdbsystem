# Python Lmdbsystem

[![Testing](https://github.com/rabiloo/python-lmdbsystem/actions/workflows/test.yml/badge.svg)](https://github.com/rabiloo/python-lmdbsystem/actions/workflows/test.yml)
[![Latest Version](https://img.shields.io/pypi/v/lmdbsystem.svg)](https://pypi.org/project/lmdbsystem)
[![Downloads](https://img.shields.io/pypi/dm/lmdbsystem.svg)](https://pypi.org/project/lmdbsystem)
[![Pypi Status](https://img.shields.io/pypi/status/lmdbsystem.svg)](https://pypi.org/project/lmdbsystem)
[![Python Versions](https://img.shields.io/pypi/pyversions/lmdbsystem.svg)](https://pypi.org/project/lmdbsystem)

## About Lmdbsystem

[LMDB Convertor](https://github.com/rabiloo/python-lmdbsystem) is a lmdb file handle library for python. It provides method to read, write to the lmdb file

## Install

```
$ pip install lmdbsystem
```

## Usage

```
from dataset_loaders import ImageLoader

from lmdbsystem.lmdb import Lmdb
from lmdbsystem.write_adapters.text import TextWriteAdapter
from lmdbsystem.write_adapters.image import ImageWriteAdapter
from lmdbsystem.read_adapters.cv2_image import Cv2ImageReadAdapter
from lmdbsystem.read_adapters.pil_image import PilImageReadAdapter
from lmdbsystem.read_adapters.bytes_image import BytesImageReadAdapter
from lmdbsystem.read_adapters.text import TextReadAdapter
from lmdbsystem.dataloader import DataLoader


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


# Write lmdb file with label in filename       
lmdb_obj = Lmdb(TextWriteAdapter(path=args.lmdb_file))
lmdb_obj.write_loader(
    LabelInFilenameLoader(
        directory=args.folder,
        suffix=args.suffix,
        fn_md5_path=args.fn_md5_path,
        values_map=values_map,
        delimiter=args.delimiter,
        values_index=values_index,
    ),
)

# Write lmdb file with image directory 
lmdb_obj = Lmdb(ImageWriteAdapter(path=args.lmdb_file, map_size=args.lmdb_map_size))
lmdb_obj.write_loader(
    ImageLoader(
        directory=args.folder,
        suffix=args.suffix,
        fn_md5_mode=args.fn_md5_mode,
        fn_md5_path=args.fn_md5_path,
    ),
)


# Read image
value = Lmdb(Cv2ImageReadAdapter(path=path)).read_index(index)
value = Lmdb(PilImageReadAdapter(path=path)).read_index(index)
value = Lmdb(BytesImageReadAdapter(path=path)).read_index(index)

# Read text
value = Lmdb(TextReadAdapter(path=path)).read_index(index)
```

## Changelog

Please see [CHANGELOG](CHANGELOG.md) for more information on what has changed recently.

## Contributing

Please see [CONTRIBUTING](.github/CONTRIBUTING.md) for details.

## Security Vulnerabilities

Please review [our security policy](../../security/policy) on how to report security vulnerabilities.

## Credits

- [Dao Quang Duy](https://github.com/duydq12)
- [All Contributors](../../contributors)

## License

The MIT License (MIT). Please see [License File](LICENSE) for more information.
