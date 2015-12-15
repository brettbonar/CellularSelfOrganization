from __future__ import division
from __future__ import print_function
import sys
import shutil
from os import environ
from os import getcwd
import string
import zlib
import bz2

import subprocess
import os
import glob
import random
random.seed()
from PIL import Image
    
lowest = 1.0
highest = 0.0

def getNcd(file1, file2, path):
  global lowest
  global highest

  size1 = os.path.getsize(file1)
  size2 = os.path.getsize(file2)


  image1 = Image.open(file1)
  image2 = Image.open(file2)

  #x, y = image1.size
  #newImage = Image.new(image1.mode, (x, y * 2))
  #newImage.paste(image1, (0, 0))
  #newImage.paste(image2, (0, y))
  #newImage.save(path + "/testimage.png", "PNG")
  ##newSize = os.path.getsize(path + "/testimage.png")
  #newSize = os.path.getsize(path + "/testimage.png")

  x, y = image1.size
  newImage = Image.new(image1.mode, (x * 2, y))
  newImage.paste(image1, (0, 0))
  newImage.paste(image2, (x, 0))
  newImage.save(path + "/testimage.png", "PNG")
  #newSize = os.path.getsize(path + "/testimage.png")
  newSize = os.path.getsize(path + "/testimage.png")


  #print(size1)
  #print(size2)
  #print(newSize)

  print(newSize)
  print(size1)
  print(size2)

  ncd = (newSize - min(size1, size2)) / (max(size1, size2))
  if (ncd < lowest):
    lowest = ncd
    shutil.copyfile(path + "/testimage.png", path + "/lowest.png")
  if (ncd > highest):
    highest = ncd
    shutil.copyfile(path + "/testimage.png", path + "/highest.png")
  print(ncd)
  return ncd

def getNcd2(file1, file2, path):
  size1 = getCSize2(file1, path)
  size2 = getCSize2(file2, path)

  with open(path + "/concatFile.test", "wb") as outfile:
    outfile.write(open(file1, "rb").read())
    outfile.write(open(file2, "rb").read())
    outfile.close()

  newSize = getCSize2(path + "/concatFile.test", path)

  print(size1)
  print(size2)
  print(newSize)

  ncd = (newSize - min(size1, size2)) / (max(size1, size2))

  print(ncd)
  return ncd

def getJpegNcd(file1, file2, path):
  global lowest
  global highest

  size1 = getJpegSize(file1, path)
  size2 = getJpegSize(file2, path)

  image1 = Image.open(file1)
  image2 = Image.open(file2)

  #x, y = image1.size
  #newImage = Image.new(image1.mode, (x, y * 2))
  #newImage.paste(image1, (0, 0))
  #newImage.paste(image2, (0, y))
  #newImage.save(path + "/testimage.png", "PNG")
  ##newSize = os.path.getsize(path + "/testimage.png")
  #newSize = getCSize(path + "/testimage.png")

  x, y = image1.size
  newImage = Image.new(image1.mode, (x * 2, y))
  newImage.paste(image1, (0, 0))
  newImage.paste(image2, (x, 0))
  newImage.save(path + "/testimage.jpeg")
  newSize = os.path.getsize(path + "/testimage.jpeg")

  print(size1)
  print(size2)
  print(newSize)

  ncd = (newSize - min(size1, size2)) / (max(size1, size2))
  if (ncd < lowest):
    lowest = ncd
    shutil.copyfile(path + "/testimage.jpeg", path + "/lowest.jpeg")
  if (ncd > highest):
    highest = ncd
    shutil.copyfile(path + "/testimage.jpeg", path + "/highest.jpeg")

  print(ncd)
  return ncd


#def getDataCSize(data):
#  compressed = zlib.compress(data, 9)
#  with open(path + "/testC", "wb") as out_file:
#      out_file.write(compressed)

#  return os.path.getsize(path + "/testC")

def getJpegSize(file, path):
  image = Image.open(file)
  image.save(path + "/testimage.jpg")
  return os.path.getsize(path + "/testimage.jpg")

def getCSize(file, path):
  with open(file, "rb") as in_file:
    compressed = zlib.compress(in_file.read(), 9)

  with open(path + "/testC", "wb") as out_file:
      out_file.write(compressed)

  return os.path.getsize(path + "/testC")

def getCSize2(file, path):
  with open(file, "rb") as in_file:
    compressed = bz2.compress(in_file.read(), 9)

  with open(path + "/testC", "wb") as out_file:
      out_file.write(compressed)

  return os.path.getsize(path + "/testC")

def setComplexityJpeg(files, path):
  sumFiles = 0
  for file1 in files:
    size1 = getJpegSize(file1, path)
    for file2 in files:
      if file1 != file2:
        ncd = getJpegNcd(file1, file2, path)
        sumFiles += size1 * ncd * (1 - ncd)
  print(sumFiles)
  return (1 / (len(files) * (len(files) - 1))) * sumFiles

def setComplexityBz2(files, path):
  sumFiles = 0
  for file1 in files:
    size1 = getCSize2(file1, path)
    for file2 in files:
      if file1 != file2:
        ncd = getNcd2(file1, file2, path)
        sumFiles += size1 * ncd * (1 - ncd)
  print(sumFiles)
  return (1 / (len(files) * (len(files) - 1))) * sumFiles

def setComplexitySimple(files, path):
  sumFiles = 0
  for file1 in files:
    size1 = os.path.getsize(file1)
    for file2 in files:
      if file1 != file2:
        ncd = getNcd(file1, file2, path)
        sumFiles += ncd * (1 - ncd)
  print(sumFiles)
  return (1 / (len(files) * (len(files) - 1))) * sumFiles

def setComplexity(files, path):
  import math
  sumFiles = 0
  for file1 in files:
    size1 = os.path.getsize(file1)
    for file2 in files:
      if file1 != file2:
        ncd = getNcd(file1, file2, path)
        #sumFiles += size1 * ncd * (1 - ncd)
        sumFiles += math.log(size1) * ncd * (1 - ncd)
  print(sumFiles)
  return (1 / (len(files) * (len(files) - 1))) * sumFiles

def getFiles():
  all_subdirs = [os.path.join(path, d) for d in os.listdir(path) if os.path.isdir(os.path.join(path, d))]
  latest_subdir = max(all_subdirs, key=os.path.getmtime)
  #files = glob.glob(latest_subdir + "/**/*.png")
  files = glob.glob(latest_subdir + "/**/*.vtk")
  return files

if __name__ == "__main__":
  path = sys.argv[1]
  files = glob.glob(path + "/**/*.png")
  print(files)
  files.sort(key=os.path.getmtime)

  testoutput = open(path + "/testoutput.txt", "w")
  #numSets = len(files) - 4
  #for i in range(0, numSets):
  #  filesSet = files[i:i+4]
  #  if (i == numSets - 1):
  #    filesSet = files[-4:]
  #  print(setComplexity(filesSet), file=testoutput)

  print(setComplexity(files, path))

  #numSets = len(files) - 2
  #for i in range(0, numSets):
  #  print(getNcd(files[i], files[i+1]), file=testoutput)

  #for file in files:
  #  print(1 / os.path.getsize(file), file=testoutput)
