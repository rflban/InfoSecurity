#!/usr/bin/env python3

import sys
import argparse

import rsa as rsa_module


def main():
    parser = create_parser()
    args = parser.parse_args(sys.argv[1:])

    rsa = rsa_module.RSA(random_seed=args.seed)
    print("public  key = %s" % str(rsa._pub))
    print("private key = %s" % str(rsa._pri))

    input_file = open(args.input_file, 'rb')
    output_file = open(args.output_file, 'wb')

    inputbytes = input_file.read()
    outputbytes = None

    if args.decrypt:
        outputbytes = rsa.decrypt(inputbytes)
    else:
        outputbytes = rsa.encrypt(inputbytes)

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
    parser.add_argument(
        'output_file',
        type=str,
        help="output file name"
    )
    parser.add_argument(
        "-s", "--seed",
        required=False, type=int, default=0,
        help="seed for generate rotors and reflector"
    )
    parser.add_argument(
        "-d", "--decrypt",
        action="store_true", default=False
    )

    return parser


if __name__ == "__main__":
    main()
