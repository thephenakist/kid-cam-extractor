#!/usr/bin/env python

# Kid Camera Exporter
# by Phenakist

# This script will extract JFIF files from a hex dump of a cheap kid's camera
# It searches for chunks that begin with the SOF marker and end with the EOF marker
# Chunks will be written to individual JFIF files which can then be converted to JPG using ffmpeg
# e.g. for i in *.jfif; do ffmpeg -i $i "`basename $i .jfif`.jpg"; done

dump_file = 'camera.bin'
sof = b'\xff\xd8'
eof = b'\xff\xd9'

with open(dump_file, 'rb') as dump:
  data = dump.read()
  chks = data.split(sof)
  for i in range(len(chks)):
    with open('img{}.jfif'.format(i), 'wb') as out:
      out.write(sof+b''.join(chks[i].split(eof)[:-1])+eof)
