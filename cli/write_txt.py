import argparse
import os

from lmdbsystem.lmdb import Lmdb
from lmdbsystem.write_adapters.text import TextWriteAdapter


def unescaped_str(arg_str):
    return arg_str.encode().decode('unicode_escape')


def get_argument():
    parser = argparse.ArgumentParser(
        description='Convert pdf file to text detection and recognition label.',
    )

    parser.add_argument('--lmdb-file',
                        type=str,
                        help='The path of lmdb file',
                        required=True)

    parser.add_argument('--files',
                        type=str,
                        help='The list of file path,'
                             'Except value: /tmp/test1.txt,/tmp/test2.txt,/tmp/test3.txt')

    parser.add_argument('--folder',
                        type=str,
                        help='Directory to containing the label file')

    parser.add_argument('--suffix',
                        default='.txt',
                        type=str,
                        help='The suffix of label file')

    parser.add_argument('--delimiter',
                        type=unescaped_str,
                        choices=['\t', '\n', ' ', ',', '_'],
                        help='punctuation for split the label line',
                        required=True)

    parser.add_argument('--key-index',
                        type=int,
                        help='The index to extract key from the label line')

    parser.add_argument('--values-index',
                        type=str,
                        help='The list of index to extract values from the label line'
                             'Except value: 0,1,2,3')

    parser.add_argument('--fn-md5-mode',
                        type=str,
                        help='The mode of handle with filename_to_md5 file. Only support ["r", "w"] mode',
                        required=True)

    parser.add_argument('--fn-md5-path',
                        type=str,
                        help='The path of filename_to_md5 file',
                        required=True)

    parser.add_argument('--pattern-value-in-key',
                        type=str,
                        help='The pattern of value in key')

    parser.add_argument('--type-value-in-key',
                        type=str,
                        choices=['int', 'str', 'float'],
                        help='The type of value in key')

    parser.add_argument('--values-map',
                        type=str,
                        help='List of normalize the value.'
                             'Ex: "Female:0,Male:1,female:0,male:1,111:1,112:0"')

    parser.add_argument('--from-filename',
                        action=argparse.BooleanOptionalAction,
                        help='Extract value from filename')
    args = parser.parse_args()
    return args


def main():
    args = get_argument()

    if not args.folder and not args.files:
        raise ValueError("Do not empty both --files and --folder argument")

    if args.folder and not os.path.isdir(args.folder):
        raise ValueError("Folder not exists")

    if args.folder and (not args.suffix or not args.values_index):
        raise ValueError("Do not empty --suffix or --values-index argument when handle with some folder")

    if args.files and args.key_index is None:
        raise ValueError("Do not empty --key-index argument when handle with some files")

    if not args.pattern_value_in_key and not args.values_index:
        raise ValueError("Do not empty both of --pattern-value-in-key and --values-index argument")

    options = {}
    if args.pattern_value_in_key:
        options["pattern_value_in_key"] = args.pattern_value_in_key
    if args.type_value_in_key:
        options["type_value_in_key"] = args.type_value_in_key
    if args.values_index:
        values_index = [int(value) for value in args.values_index.split(",")]
        options["values_index"] = values_index
    if args.values_map:
        values_map = {value.split(":")[0]: value.split(":")[1] for value in args.values_map.split(",")}
        options["values_map"] = values_map
    if args.from_filename:
        options["from_filename"] = args.from_filename

    options["delimiter"] = args.delimiter

    if args.files:
        file_paths = args.files.split(",")
        options["key_index"] = args.key_index

        lmdb_obj = Lmdb(TextWriteAdapter(path=args.lmdb_file))
        lmdb_obj.write_files(
            file_paths=file_paths,
            fn_md5_mode=args.fn_md5_mode,
            fn_md5_path=args.fn_md5_path,
            options=options,
        )
    else:
        lmdb_obj = Lmdb(TextWriteAdapter(path=args.lmdb_file))
        lmdb_obj.write_dir(
            directory=args.folder,
            suffix=args.suffix,
            fn_md5_mode=args.fn_md5_mode,
            fn_md5_path=args.fn_md5_path,
            options=options,
        )


if __name__ == '__main__':
    main()
