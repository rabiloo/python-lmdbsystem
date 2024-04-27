import argparse

from lmdbsystem.lmdb import Lmdb
from lmdbsystem.write_adapters.csv import CsvWriteAdapter


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
                             'Except value: /tmp/test1.csv,/tmp/test2.csv,/tmp/test3.csv',
                        required=True)

    parser.add_argument('--suffix',
                        default='.csv',
                        type=str,
                        help='The suffix of label file')

    parser.add_argument('--delimiter',
                        type=unescaped_str,
                        choices=['\t', '\n', ' ', ',', '_'],
                        help='punctuation for split the label line',
                        required=True)

    parser.add_argument('--key-index',
                        type=int,
                        help='The index to extract key from the label line',
                        required=True)

    parser.add_argument('--values-index',
                        type=str,
                        help='The list of index to extract values from the label line'
                             'Except value: 0,1,2,3',
                        required=True)

    parser.add_argument('--fn-md5-mode',
                        type=str,
                        help='The mode of handle with filename_to_md5 file. Only support ["r", "w"] mode',
                        required=True)

    parser.add_argument('--fn-md5-path',
                        type=str,
                        help='The path of filename_to_md5 file',
                        required=True)

    parser.add_argument('--values-map',
                        type=str,
                        help='List of normalize the value.'
                             'Ex: "Female:0,Male:1,female:0,male:1,111:1,112:0"')

    parser.add_argument('--skip-header',
                        action=argparse.BooleanOptionalAction,
                        help='ignore header of csv if True, default False')

    args = parser.parse_args()
    return args


def main():
    args = get_argument()

    options = {}
    if args.values_index:
        values_index = [int(value) for value in args.values_index.split(",")]
        options["values_index"] = values_index
    if args.values_map:
        values_map = {value.split(":")[0]: value.split(":")[1] for value in args.values_map.split(",")}
        options["values_map"] = values_map
    if args.skip_header:
        options["skip_header"] = args.skip_header

    options["delimiter"] = args.delimiter

    file_paths = args.files.split(",")
    options["key_index"] = args.key_index

    lmdb_obj = Lmdb(CsvWriteAdapter(path=args.lmdb_file))
    lmdb_obj.write_files(
        file_paths=file_paths,
        fn_md5_mode=args.fn_md5_mode,
        fn_md5_path=args.fn_md5_path,
        options=options,
    )


if __name__ == '__main__':
    main()
