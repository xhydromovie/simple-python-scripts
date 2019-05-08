from PIL import Image
import os
import argparse
import ffmpy

''' 
Simple python script that reduce size of jpg, mp4, wmv files.
Created for my django project.

Usage: python3 reducemediafiles.py path_to_dir
'''

parser = argparse.ArgumentParser(description="Type path name")
parser.add_argument('path', help="Type path")
args = parser.parse_args()
path = args.path
path_compressed = path + "/compressed"

count = 0
processed = 0
all_files = 0
not_supported = 0
jpg = 0
wmv = 0
mp4 = 0
others = []

try:
    os.mkdir(path_compressed)
except:
    print("Dir exists")

#Count all files
for filename in os.listdir(path):
    count = count + 1

for filename in os.listdir(path):
    all_files = all_files + 1
    filetype = filename.split(".")[-1]

    if filetype == "jpg":
        jpg = jpg + 1
        processed = processed+1
        print("Copressing picture {}, id: {}/{}".format(filename, processed, count))
        img = Image.open(path + "/" + filename)
        img.save(path_compressed + "/" + filename, quality=50, optimize=True)
    elif filetype == "wmv" or filetype == "mp4":
        processed = processed+1

        if filetype == "wmv":
            wmv = wmv + 1
        elif filetype == "mp4":
            mp4 = mp4 + 1

        print("Copressing video {}, id: {}/{}".format(filename, processed, count))
        ff = ffmpy.FFmpeg(
            inputs={path + "/" + filename: None},
            outputs={path_compressed + "/" + filename: '-crf 30 -vcodec libx264 -loglevel panic' },
            )
        ff.run()
    else:
        others.append(filename)
        print("File not supported...")
        not_supported = not_supported + 1

print("\n\n")
print("Processing finished!")
print("Files processed: {}/{}. Not supported: {}".format(processed, all_files, not_supported))
print("Type JPG: {}, MP4: {}, WMV: {}".format(jpg, mp4, wmv))
print("Others:", *others)
