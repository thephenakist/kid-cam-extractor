# Kid Cam Extractor
Hey all! I initially posted these instructions on Reddit, but my account got banned for some reason.

These are instructions for how to access the photos on the internal memory of that cheap kid's camera.

The internal images are stored in an SPI NOR chip with a model P25D32H. This chip can be read with a [CH341A USB reader](https://www.amazon.com/dp/B07RV35D4B) and [NeoProgrammer](https://github.com/GioLangLe/CH341B-NeoProgramer). The chip is a 25xx chip and I was able to load it using the config for P25QD32H.

The images are stored in JFIF format. More details about the file format can be found [here](https://en.wikipedia.org/wiki/JPEG_File_Interchange_Format) but the important info is that the images start with the hex values FF D8 and end with FF D9.

I wrote a python script (see below) and was able to split the hex dump from NeoProgrammer using these SOF / EOF markers, writing each chunk to an individual file.

You can then use ffmpeg to convert the jfif files to jpg.

Here's the python script I wrote to split the hex dump:

```
dump_file = 'kid_camera.bin'
sof = b'\xff\xd8'
eof = b'\xff\xd9'

with open(dump_file, 'rb') as dump:
  data = dump.read()
  chks = data.split(sof)
  for i in range(len(chks)):
    with open('img{}.jfif'.format(i), 'wb') as out:
      out.write(sof+chks[i].split(eof)[0]+eof)
```
