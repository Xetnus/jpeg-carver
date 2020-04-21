import sys
import os

filename = sys.argv[1]
jpeg_header = "FFD8FF"
jpeg_trailer = "FFD9"
block_counter = 0
start = 0
image_num = 0
header_found = False

with open(filename, "rb") as file:
    while True:
        hex_string = ""
        block = file.read(512)
        for i in block:
            hex_string += "%0.2X" % i

        if not hex_string:
            break

        if not header_found and jpeg_header in hex_string:
            image_num += 1
            print("=============== Image %i ===============" % image_num)
            print("JPEG header found in block %i" % block_counter)
            start = block_counter
            header_found = True

        if header_found and jpeg_trailer in hex_string:
            # Ensure trailer is byte-oriented
            if hex_string.find(jpeg_trailer) % 2 == 0:
                print("JPEG trailer found in block %i" % block_counter)
                count = block_counter - start + 1
                print("Count %i" % (count))
                os.system("dd if={} of=image{}.jpeg skip={} count={}".format(filename, image_num, start, count))
                print("Image copied to image%i.jpeg\n=======================================" % image_num)
                header_found = False

        block_counter += 1

print("%i Image(s) Found" % image_num)
