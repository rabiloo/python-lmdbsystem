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
from file_verifier.mime.magic_async_mime import MagicAsyncValidatorMime
from file_verifier.size.basic_async_size import BaseAsyncValidatorSize
from file_verifier.type.filetype_type import FiletypeValidatorType
from file_verifier.convertor.pillow_convertor import PillowConvertor
from file_verifier.file_validator import FileValidator


mime_validator = MagicAsyncValidatorMime(acceptable_mimes=["image/jpeg"])
size_validator =  BaseAsyncValidatorSize(max_upload_file_size=1024 * 1024)
type_validator = FiletypeValidatorType(acceptable_types=["image"])
file_convertor = PillowConvertor(acceptable_mimes=["image/jpeg"])

obj_validator = FileValidator(mime_validator, size_validator, type_validator, file_convertor)

obj_validator.validate_file("/tmp/hello.txt")
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
