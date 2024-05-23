import argparse

from cli.dataset_loaders import LabelInSomeCsvLoader
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

    parser.add_argument(
        "--values-index",
        type=str,
        help="The list of index to extract values from the label line, Except value: 0,1,2,3",
        required=True,
    )

    parser.add_argument("--fn-md5-path", type=str, help="The path of filename_to_md5 file", required=True)

    parser.add_argument(
        "--values-map",
        type=str,
        help="List of normalize the value." 'Ex: "Female:0,Male:1,female:0,male:1,111:1,112:0"',
    )

    parser.add_argument(
        "--skip-header", action=argparse.BooleanOptionalAction, help="ignore header of csv if True, default False"
    )
    args = parser.parse_args()
    return args


def main():
    args = get_argument()

    values_index = [int(value) for value in args.values_index.split(",")]
    values_map = (
        {value.split(":")[0]: value.split(":")[1] for value in args.values_map.split(",")} if args.values_map else None
    )

    lmdb_obj = Lmdb(TextWriteAdapter(path=args.lmdb_file))
    lmdb_obj.write_loader(
        LabelInSomeCsvLoader(
            file_paths=args.files.split(","),
            fn_md5_path=args.fn_md5_path,
            key_index=args.key_index,
            values_index=values_index,
            values_map=values_map,
            delimiter=args.delimiter,
            skip_header=args.skip_header | False,
        ),
    )


if __name__ == "__main__":
    main()
