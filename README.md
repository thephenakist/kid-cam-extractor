# Kid Cam Extractor
I originally posted these instructions on Reddit [here](https://www.reddit.com/r/AskElectronics/comments/15zgc1u/comment/mic2ws1/), but my account got flagged for some reaason and those comments appear to be lost to time.

These are instructions for how to access the photos on the internal memory of a popular [kid's camera](https://www.amazon.com/dp/B087ZTH98B).

The images are stored along with the firmware in an onboard chip in JFIF format. More details about the JFIF file format can be found [here](https://en.wikipedia.org/wiki/JPEG_File_Interchange_Format) but the important info is that the images start with the hex values `FF D8` and end with `FF D9`.

I was able to export the firmware from the onboard chip and then write a Python script to split the hex dump from NeoProgrammer using the JFIF SOF / EOF markers, writing each chunk to an individual file.

I then used ffmpeg to convert the resulting jfif files to jpg.

# Instructions

## Extract Firmware From Camera
The internal images are stored in an SPI NOR chip with a model [P25D32H](https://www.lcsc.com/product-detail/C5263842.html). When you open the camera, you're looking for a small black microchip with 8 spider legs coming out of it. The contents of this chip can be read by connecting it to a [CH341A USB reader](https://www.amazon.com/dp/B07RV35D4B) and using [NeoProgrammer](https://github.com/GioLangLe/CH341B-NeoProgramer) to dump the firmware. The chip is a 25xx chip, so use the config for P25QD32H. Dump the firmware from the chip and save it as `camera.bin`.

## Extract Images From Dump File
Download extract.py from this repo and put it in the same folder as the `camera.bin` you dumped from the camera's chip, then execute the Python script. This will dump all of the images from the bin file into the same folder. You should end up with a bunch of img[#].jfif files which can then be converted to jpeg using FFmpeg. The first 60 or so images are actually part of the firmware and are the different backgrounds and overlays used by the camera OS, such as the startup image here:

![Welcome screen image used by the camera](https://github.com/thephenakist/kid-cam-extractor/blob/main/Overlays/out50.jpg?raw=true)

## Convert JFIF Files To JPEG
If you're not familiar with [FFmpeg](https://www.ffmpeg.org/download.html), here's an example of how to use the command:

```
ffmpeg -i out1.jfif out1.jpg
```