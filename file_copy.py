import os
import sys

CHUNKSIZE = 50000

fn1 = input("File to copy from> ")
if not os.path.exists(fn1):
    print("No such file")
    sys.exit(1)

fn2 = input("File to write to > ")

fp1 = open(fn1, "rb")
fp2 = open(fn2, "wb")

while (d := fp1.read(CHUNKSIZE)):
    fp2.write(d)