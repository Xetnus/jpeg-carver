from dd import carve
import sys
import os
import argparse
import shutil


def create_dump_dir(output_dir="output"):
    if os.path.isdir(output_dir):
        usr = input("Output directory already exists, do you want to delete \
            it? [y/n] ").lower()
        if usr == 'y':
            shutil.rmtree(output_dir)
        else:
            exit()
    os.mkdir(output_dir)


def main(filename: str):
    create_dump_dir()
    jpeg_header = bytes.fromhex("FFD8FF")
    jpeg_trailer = bytes.fromhex("FFD9")
    start = 0
    image_num = 0
    header_found = False
    offset = 0

    with open(filename, "rb") as file:  # open bin file
        for i in range(os.path.getsize(filename)):
            if header_found:  # Getting trailer tag
                search = file.read(len(jpeg_trailer))  # get tag
                file.seek((1 - len(jpeg_trailer)), os.SEEK_CUR) # move back
            else:             # Getting Header tag
                search = file.read(len(jpeg_header))
                file.seek((1 - len(jpeg_header)), os.SEEK_CUR)
            
            if search == jpeg_header and not header_found:
                print("Found Header at " + str(i))
                offset = i              # We found the start header, mark offset
                header_found = True     # Mark flag, start search for trailer

            elif search == jpeg_trailer and header_found:
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
    #parser.add_argument("--output_directory", "-o")
    args = parser.parse_args()
    main(args.filename)

