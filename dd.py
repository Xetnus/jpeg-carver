import argparse


def carve(filename: str, bytes: int, output: str, s_offset=0, verbose=False):
    """
    Carve 'bytes' out of file 'filename', with optional starting offset
    's_offset'.
    If the bytes to take out is larger than
    """
    with open(filename, "rb") as binary:
        binary.seek(s_offset)
        with open(output, "wb") as binary_out:
            carving = binary.read(bytes)
            binary_out.write(carving)
            if verbose:
                print(str(carving))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Simplistic Python dd')
    parser.add_argument("filename", type=str,
        help="file to carve from")
    parser.add_argument('bytes', type=int,
        help="Bytes to carve out")
    parser.add_argument('output', type=str,
        help="File to output bytes to, WILL overwrite a previous file")
    parser.add_argument('offset', type=int, nargs='?', default=0,
    help="Optional starting byte offset")
    args = parser.parse_args()
    carve(args.filename, args.bytes, args.output, args.offset)
