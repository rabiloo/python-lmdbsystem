import argparse
import os

from lmdbsystem.lmdb import Lmdb
from lmdbsystem.write_adapters.json_facepp import JsonFaceppWriteAdapter


def get_argument():
    parser = argparse.ArgumentParser(
        description="Convert pdf file to text detection and recognition label.",
    )

    parser.add_argument("--lmdb-file", type=str, help="The path of lmdb file", required=True)

    parser.add_argument("--folder", type=str, help="Directory to containing the label file", required=True)

    parser.add_argument("--suffix", default=".json", type=str, help="The suffix of label file")

    parser.add_argument(
        "--fn-md5-mode",
        type=str,
        help='The mode of handle with filename_to_md5 file. Only support ["r", "w"] mode',
        required=True,
    )

    parser.add_argument("--fn-md5-path", type=str, help="The path of filename_to_md5 file", required=True)

    parser.add_argument(
        "--keys-extracted",
        type=str,
        choices=[
            "gender,value",
            "age,value",
            "headpose",
            "emotion",
            "facequality,value",
            "ethnicity,value",
            "beauty",
            "glass,value",
        ],
        help="The key with multi level to extract from the label file",
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

    if args.folder and not os.path.isdir(args.folder):
        raise ValueError("Folder not exists")

    if args.folder and not args.suffix:
        raise ValueError("Do not empty --suffix argument when handle with some folder")

    keys_extracted = args.keys_extracted.split(",") if args.keys_extracted else []
    options = {
        "keys_extracted": keys_extracted,
    }

    if args.values_map:
        values_map = {value.split(":")[0]: value.split(":")[1] for value in args.values_map.split(",")}
        options["values_map"] = values_map

    lmdb_obj = Lmdb(JsonFaceppWriteAdapter(path=args.lmdb_file))
    lmdb_obj.write_dir(
        directory=args.folder,
        suffix=args.suffix,
        fn_md5_mode=args.fn_md5_mode,
        fn_md5_path=args.fn_md5_path,
        options=options,
    )


if __name__ == "__main__":
    main()
