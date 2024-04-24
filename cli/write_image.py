import argparse

from lmdbsystem.lmdb import Lmdb
from lmdbsystem.write_adapters.image import ImageWriteAdapter


def get_argument():
    parser = argparse.ArgumentParser(description='Convert pdf file to text detection and recognition label.')

    parser.add_argument('--lmdb-file',
                        type=str,
                        help='The path of lmdb file',
                        required=True)

    parser.add_argument('--folder',
                        type=str,
                        help='Directory to containing the image file',
                        required=True)

    parser.add_argument('--suffix',
                        default='.jpg',
                        type=str,
                        help='The suffix of image file')

    parser.add_argument('--fn-md5-mode',
                        type=str,
                        help='The mode of handle with filename_to_md5 file. Only support ["r", "w"] mode',
                        required=True)

    parser.add_argument('--fn-md5-path',
                        type=str,
                        help='The path of filename_to_md5 file',
                        required=True)

    args = parser.parse_args()
    return args


def main():
    args = get_argument()

    lmdb_obj = Lmdb(ImageWriteAdapter(path=args.lmdb_file))
    lmdb_obj.write_dir(
        directory=args.folder,
        suffix=args.suffix,
        fn_md5_mode=args.fn_md5_mode,
        fn_md5_path=args.fn_md5_path,
    )


if __name__ == '__main__':
    main()
