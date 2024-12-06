# pybase64_reddy/cli.py

import argparse
from . import encode, decode

def main():
    parser = argparse.ArgumentParser(
        description='A simple base64 encode/decode tool.'
    )
    subparsers = parser.add_subparsers(
        title='Commands',
        dest='command',
        required=True,
        help='Available commands'
    )

    # Encode command
    encode_parser = subparsers.add_parser(
        'encode',
        help='Encode a string to base64.'
    )
    encode_parser.add_argument(
        'string',
        type=str,
        help='The string to encode.'
    )

    # Decode command
    decode_parser = subparsers.add_parser(
        'decode',
        help='Decode a base64 string.'
    )
    decode_parser.add_argument(
        'string',
        type=str,
        help='The base64 string to decode.'
    )

    args = parser.parse_args()

    if args.command == 'encode':
        result = encode(args.string)
        print(result)
    elif args.command == 'decode':
        try:
            result = decode(args.string)
            print(result)
        except ValueError as e:
            print(f"Error: {e}")
