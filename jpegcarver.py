from dd import carve
import sys
import os
import argparse
import shutil

BLOCK = 512
START = 20  # max length the header could be in the starting block
JPEG_HEADER = bytes.fromhex("FFD8FF")
JPEG_TRAILER = bytes.fromhex("FFD9")
EXIF_HEADER = bytes.fromhex("FFE1")
JPEG_EXIF_HEADER_LEN = 6  # includes JPEG header, exif header, and exif length field

def create_dump_dir(output_dir="output"):
    if os.path.isdir(output_dir):
        dir_exists = "Output directory already exists, do you want to delete it? [y/n] "
        usr = input(dir_exists).lower()
        if usr == 'y':
            shutil.rmtree(output_dir)
        else:
            exit()
    os.mkdir(output_dir)


def main(filename: str):
    create_dump_dir()
    start = 0
    image_num = 0
    header_found = False
    exif_found = False
    exif_data_end = 0
    offset = 0

    with open(filename, "rb") as file:  # open bin file
        for i in range(os.path.getsize(filename)):
            search_len = len(JPEG_TRAILER) if header_found else JPEG_EXIF_HEADER_LEN
            search = file.read(search_len)  # get tag
            file.seek((1 - search_len), os.SEEK_CUR)

            if JPEG_HEADER in search and not header_found and (i%BLOCK) < START:
                offset = i              # We found the start header, mark offset
                header_found = True     # Mark flag, start search for trailer

                if EXIF_HEADER in search:
                    exif_data_end = int.from_bytes(search[-2:], byteorder='big')
                    exif_data_end += i + JPEG_EXIF_HEADER_LEN
                    exif_found = True

            elif search == JPEG_TRAILER and header_found:
                # Sometimes a JPEG trailer can be found at the end of exif data.
                # However, these trailers aren't meant to end the JPEG, so skip them.
                if (exif_found and exif_data_end > i):
                    continue

                image_name = "output/image{}.jpg".format(image_num)
                print("Image found at b'{}' of length b'{}'\t{}"
                    .format(offset, (i - offset), image_name))
                # i - offset gives file size, +2 for trailer
                carve(filename, (i - offset + 2), image_name, offset)
                image_num += 1
                header_found = False
                exif_found = False

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='JPEG carving tool')
    parser.add_argument("filename", type=str,
        help="File to attempt JPEG extraction on")
    args = parser.parse_args()
    main(args.filename)
