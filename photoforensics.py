#!/usr/local/bin/python
import sys
import subprocess
import os
import json
import argparse
import hashlib
import glob

from exiftool import ExifTool

interestingTags = ["-FileName", "-GPSLatitude", "-GPSLongitude", "-GPSLatitudeRef", "-GPSLongitudeRef", "-Make", "-Model", "-SerialNumber", "-InternalSerialNumber", "-ImageUniqueID", "-Software", "-Lens", "-LensMake", "-LensModel", "-LensSerialNumber", "-Artist", "-Copyright", "-CopyrightNotice", "-Creator", "-OwnerName"]

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("files", nargs='+',metavar="path", type=str, help="One or more images to process")
    parser.add_argument("-e", "--exiftool",metavar="path", type=str, help="Exiftool executable, eg '/usr/bin/exiftool'. By default, we'll assume exiftool is on the PATH")
    args = parser.parse_args()
    # print(args.files[0])

    # print('exiftool', args.exiftool)

    files = args.files

    # if we're on windows the glob won't be pre-evaluated
    if len(files) == 1 and "*" in files[0]:
        files = glob.glob(files[0])

    exiftool = 'exiftool'
    if args.exiftool != None:
        exiftool = args.exiftool

    with ExifTool(exiftool) as e:
        metadatas = e.get_tags_batch(interestingTags, files)

        for fileName, metadata in zip(files, metadatas):
            with open(fileName, 'rb') as imageFile:
                md5 = hashlib.md5()
                sha1 = hashlib.sha1()
                buffer = imageFile.read()
                md5.update(buffer)
                sha1.update(buffer)
                metadata['md5'] = md5.hexdigest()
                metadata['sha1'] = sha1.hexdigest()

        print json.dumps(metadatas)