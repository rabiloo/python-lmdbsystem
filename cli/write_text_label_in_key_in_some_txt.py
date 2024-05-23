import argparse

from cli.dataset_loaders import LabelInKeyInSomeTxtLoader
from lmdbsystem.lmdb import Lmdb
from lmdbsystem.write_adapters.text import TextWriteAdapter


def unescaped_str(arg_str):
    return arg_str.encode().decode("unicode_escape")


def get_argument():
    parser = argparse.ArgumentParser(
        description="Convert pdf file to text detection and recognition label.",
    )

    parser.add_argument("--lmdb-file", type=str, help="The path of lmdb file", required=True)

    parser.add_argument(
        "--files",
        type=str,
        help="The list of file path, Except value: /tmp/test1.txt,/tmp/test2.txt,/tmp/test3.txt",
        required=True,
    )

    parser.add_argument(
        "--delimiter",
        type=unescaped_str,
        choices=["\t", "\n", " ", ",", "_"],
        help="punctuation for split the label line",
        required=True,
    )

    parser.add_argument("--key-index", type=int, help="The index to extract key from the label line", required=True)

    parser.add_argument("--fn-md5-path", type=str, help="The path of filename_to_md5 file", required=True)

    parser.add_argument(
        "--pattern-value-in-key",
        type=str,
        help="The pattern of value in key",
        required=True,
    )

    parser.add_argument(
        "--type-value-in-key",
        type=str,
        choices=["int", "str", "float"],
        help="The type of value in key",
        required=True,
    )

    parser.add_argument(
        "--values-map",
        type=str,
        help="List of normalize the value." 'Ex: "Female:0,Male:1,female:0,male:1,111:1,112:0"',
    )

    args = parser.parse_args()
    return args


def main():
    args = get_argument()

    values_map = (
        {value.split(":")[0]: value.split(":")[1] for value in args.values_map.split(",")} if args.values_map else None
    )

    lmdb_obj = Lmdb(TextWriteAdapter(path=args.lmdb_file))
    lmdb_obj.write_loader(
        LabelInKeyInSomeTxtLoader(
            file_paths=args.files.split(","),
            fn_md5_path=args.fn_md5_path,
            key_index=args.key_index,
            pattern_value_in_key=args.pattern_value_in_key,
            type_value_in_key=args.type_value_in_key,
            values_map=values_map,
            delimiter=args.delimiter,
        ),
    )


if __name__ == "__main__":
    main()
