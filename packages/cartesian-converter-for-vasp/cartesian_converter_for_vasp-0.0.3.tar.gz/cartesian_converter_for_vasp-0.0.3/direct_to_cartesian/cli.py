import argparse
from .DataFile import DataFile
from .DataFileHandler import DataFileHandler

def main():
    parser = argparse.ArgumentParser(
        description='Direct to cartesian from cartesian coordinates'
    )

    parser.add_argument(
        '--input', '-i',
        required=True,
        type=str,
        help='input file'
    )


    parser.add_argument(
        '--output', '-o',
        required=True,
        type=str,
        help='Output file name'
    )

    args = parser.parse_args()
    data = DataFile(args.input)
    handler = DataFileHandler(data, args.output)
    handler.save_file_after_converted()


if __name__ == '__main__':
    main()
