# jpeg-carver

`python3 jpegcarver.py <filename>`

Once you have the starting and ending blocks of the JPEG, you can run this command to extract it:
`dd if=<filename> of=output.jpeg skip=<starting_block> count=<ending_block - starting_block + 1>`
