"""
label of data in txt file, and map 1:1 with image
ex: 12_0_0_20170117190914091
"""

import argparse
import os

from cli.dataset_loaders import LabelInTxtLoader
from lmdbsystem.lmdb import Lmdb
from lmdbsystem.write_adapters.text import TextWriteAdapter


def unescaped_str(arg_str):
    return arg_str.encode().decode("unicode_escape")


def get_argument():
    parser = argparse.ArgumentParser(
        description="Convert pdf file to text detection and recognition label.",
    )

    parser.add_argument("--lmdb-file", type=str, help="The path of lmdb file", required=True)

    parser.add_argument("--folder", type=str, help="Directory to containing the label file")

    parser.add_argument("--suffix", default=".txt", type=str, help="The suffix of label file", required=True)

    parser.add_argument(
        "--delimiter",
        type=unescaped_str,
        choices=["\t", "\n", " ", ",", "_"],
        help="punctuation for split the label line",
        required=True,
    )

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

    parser.add_argument("--from-filename", action=argparse.BooleanOptionalAction, help="Extract value from filename")
    args = parser.parse_args()
    return args


def main():
    args = get_argument()
    if args.folder and not os.path.isdir(args.folder):
        raise ValueError("Folder not exists")

    values_index = [int(value) for value in args.values_index.split(",")]
    values_map = (
        {value.split(":")[0]: value.split(":")[1] for value in args.values_map.split(",")} if args.values_map else None
    )

    lmdb_obj = Lmdb(TextWriteAdapter(path=args.lmdb_file))
    lmdb_obj.write_loader(
        LabelInTxtLoader(
            directory=args.folder,
            suffix=args.suffix,
            fn_md5_path=args.fn_md5_path,
            values_map=values_map,
            delimiter=args.delimiter,
            values_index=values_index,
        ),
    )


if __name__ == "__main__":
    main()
