#!/usr/bin/env python3
import sys
import argparse

import huffman


def main():
    parser = create_parser()
    args = parser.parse_args(sys.argv[1:])

    output_file_name = args.input_file + ('.dec' if args.extract else '.bin')

    input_file = open(args.input_file, 'rb')
    output_file = open(output_file_name, 'wb')

    outputbytes = b''

    if args.extract:
        outputbytes = huffman.extract(*huffman.parse_compressed(input_file))
    else:
        outputbytes = huffman.compress(input_file.read())

    output_file.write(outputbytes)

    input_file.close()
    output_file.close()


def create_parser():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        'input_file',
        type=str,
        help="input file name"
    )
    # parser.add_argument(
        # 'output_file',
        # type=str,
        # help="output file name"
    # )
    parser.add_argument(
        "-x", "--extract",
        action="store_true", default=False
    )

    return parser


if __name__ == "__main__":
    main()
