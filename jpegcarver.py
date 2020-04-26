from dd import carve
import sys
import os
import argparse
import shutil

BLOCK = 512
START = 20  # max length the header could be in the starting block
JPEG_HEADER = bytes.fromhex("FFD8FF")
JPEG_TRAILER = bytes.fromhex("FFD9")

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
    offset = 0

    with open(filename, "rb") as file:  # open bin file
        for i in range(os.path.getsize(filename)):
            if header_found:  # Getting trailer tag
                search = file.read(len(JPEG_TRAILER))  # get tag
                file.seek((1 - len(JPEG_TRAILER)), os.SEEK_CUR) # move back
            else:             # Getting Header tag
                search = file.read(len(JPEG_HEADER))
                file.seek((1 - len(JPEG_HEADER)), os.SEEK_CUR)

            if search == JPEG_HEADER and not header_found and (i%BLOCK) < START:
                print("Found Header at " + str(i))
                offset = i              # We found the start header, mark offset
                header_found = True     # Mark flag, start search for trailer

            elif search == JPEG_TRAILER and header_found:
                # disgusting
                print("Image found at " + "b'" + str(offset) + "' of length " \
                + "b'" + str(i - offset) + "'\t image" + str(image_num) +".jpg")
                # i - offset gives file size, +2 for trailer
                carve(filename, (i - offset + 2), "output/image" +
                    str(image_num) + ".jpg", offset)
                image_num += 1
                header_found = False


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='JPEG carving tool')
    parser.add_argument("filename", type=str,
        help="File to attempt JPEG extraction on")
    args = parser.parse_args()
    main(args.filename)
