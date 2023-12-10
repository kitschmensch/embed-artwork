# embed-artwork
A simple python script to embed artwork in FLAC files using images in the same directory. Written quickly for the purpose of fixing the album art on the Sony NW-A55 DAP.

## Background
My music library has artwork stored within each directory in a file like `cover.jpg`. I avoid using embedded artwork because it's redundant: you have the same image file stored for every track on your album.

However, my DAP, the Sony NW-A55 is particularly picky about artwork. The artwork must be:
1. embedded in the file.
2. exactly square (300 x 300 pixels).
3. non-progressive JPEG.

# Usage
Execute the script with variables for folder path and "depth" (optional, in case you nest your music in Artist or Genre folders).

`python embed.py /Volumes/SD_CARD/MUSIC 3`

**Warning! Using this script permanently alters the targeted FLAC files. I'd recommend ONLY using this on the SD card that you copy music to.**
