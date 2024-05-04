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
from lmdbsystem.lmdb import Lmdb
from lmdbsystem.write_adapters.text import TextWriteAdapter
from lmdbsystem.write_adapters.image import ImageWriteAdapter
from lmdbsystem.read_adapters.cv2_image import Cv2ImageReadAdapter
from lmdbsystem.read_adapters.pil_image import PilImageReadAdapter
from lmdbsystem.read_adapters.bytes_image import BytesImageReadAdapter
from lmdbsystem.read_adapters.text import TextReadAdapter


# Write lmdb file with some label files
lmdb_obj = Lmdb(TextWriteAdapter(path=args.lmdb_file))
lmdb_obj.write_files(
    file_paths=file_paths,
    fn_md5_mode=args.fn_md5_mode,
    fn_md5_path=args.fn_md5_path,
    options=options,
)

# Write lmdb file with label directory       
lmdb_obj = Lmdb(TextWriteAdapter(path=args.lmdb_file))
lmdb_obj.write_dir(
    directory=args.folder,
    suffix=args.suffix,
    fn_md5_mode=args.fn_md5_mode,
    fn_md5_path=args.fn_md5_path,
    options=options,
)

# Write lmdb file with image directory 
lmdb_obj = Lmdb(ImageWriteAdapter(path=args.lmdb_file, map_size=args.lmdb_map_size))
lmdb_obj.write_dir(
    directory=args.folder,
    suffix=args.suffix,
    fn_md5_mode=args.fn_md5_mode,
    fn_md5_path=args.fn_md5_path,
)

# Read image
value = Lmdb(Cv2ImageReadAdapter(path=path)).read(index)
value = Lmdb(PilImageReadAdapter(path=path)).read(index)
value = Lmdb(BytesImageReadAdapter(path=path)).read(index)

# Read text
value = Lmdb(TextReadAdapter(path=path)).read(index)
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
