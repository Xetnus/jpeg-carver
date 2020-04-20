import sys

filename = sys.argv[1]
jpeg_header = "FFD8FF"
jpeg_trailer = "FFD9"
block_counter = 0
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
            print("JPEG header found in block %i" % block_counter)
            header_found = True

        if header_found and jpeg_trailer in hex_string:
            # Ensure trailer is byte-oriented
            if hex_string.find(jpeg_trailer) % 2 == 0:
                print("JPEG trailer found in block %i" % block_counter)
                header_found = False

        block_counter += 1