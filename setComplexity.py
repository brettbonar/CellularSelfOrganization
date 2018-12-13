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

def getNcdPng(file1, file2, path):
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
  newSize = os.path.getsize(path + "/testimage.png")

  ncd = (newSize - min(size1, size2)) / (max(size1, size2))
  #if (ncd < lowest):
  #  lowest = ncd
  #  shutil.copyfile(path + "/testimage.png", path + "/lowest.png")
  #if (ncd > highest):
  #  highest = ncd
  #  shutil.copyfile(path + "/testimage.png", path + "/highest.png")

  return ncd

def getNcdGray(file1, file2, path):
  size1 = getSizeGray(file1, path)
  size2 = getSizeGray(file2, path)

  image1 = Image.open(file1).convert("L")
  image2 = Image.open(file2).convert("L")

  x, y = image1.size
  newImage = Image.new(image1.mode, (x * 2, y))
  newImage.paste(image1, (0, 0))
  newImage.paste(image2, (x, 0))
  newImage.save(path + "/testimage.png", "PNG")
  newSize = os.path.getsize(path + "/testimage.png")
  os.remove(path + "/testimage.png")

  ncd = (newSize - min(size1, size2)) / (max(size1, size2))

  print(ncd)

  return ncd

def getNcdBz2(file1, file2, path):
  size1 = getCSizeBz2(file1, path)
  size2 = getCSizeBz2(file2, path)

  with open(path + "/concatFile.test", "wb") as outfile:
    outfile.write(open(file1, "rb").read())
    outfile.write(open(file2, "rb").read())
    outfile.close()

  newSize = getCSizeBz2(path + "/concatFile.test", path)

  ncd = (newSize - min(size1, size2)) / (max(size1, size2))

  return ncd

def getNcdZip(file1, file2, path):
  size1 = getCSizeZip(file1, path)
  size2 = getCSizeZip(file2, path)

  with open(path + "/concatFile.test", "wb") as outfile:
    outfile.write(open(file1, "rb").read())
    outfile.write(open(file2, "rb").read())
    outfile.close()

  newSize = getCSizeZip(path + "/concatFile.test", path)

  ncd = (newSize - min(size1, size2)) / (max(size1, size2))

  return ncd

def getJpegNcd(file1, file2, path):
  size1 = getJpegSize(file1, path)
  size2 = getJpegSize(file2, path)

  image1 = Image.open(file1).convert("L")
  image2 = Image.open(file2).convert("L")

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
  newImage.save(path + "/testimage.jpg", "JPEG", quality=10)
  newSize = os.path.getsize(path + "/testimage.jpg")

  ncd = (newSize - min(size1, size2)) / (max(size1, size2))
  #if (ncd < lowest):
  #  lowest = ncd
  #  shutil.copyfile(path + "/testimage.jpeg", path + "/lowest.jpeg")
  #if (ncd > highest):
  #  highest = ncd
  #  shutil.copyfile(path + "/testimage.jpeg", path + "/highest.jpeg")
  
  print(ncd)

  return ncd


#def getDataCSize(data):
#  compressed = zlib.compress(data, 9)
#  with open(path + "/testC", "wb") as out_file:
#      out_file.write(compressed)

#  return os.path.getsize(path + "/testC

def getSizeGray(file, path):
  image = Image.open(file).convert("L")

  image.save(path + "/testimage.png", "PNG")
  size = os.path.getsize(path + "/testimage.png")
  os.remove(path + "/testimage.png")

  return size

def getJpegSize(file, path):
  image = Image.open(file).convert("L")
  image.save(path + "/testimage.jpg", "JPEG", quality=10)
  return os.path.getsize(path + "/testimage.jpg")

def getCSizeBz2(file, path):
  with open(file, "rb") as in_file:
    compressed = bz2.compress(in_file.read(), 1)

  with open(path + "/testC", "wb") as out_file:
      out_file.write(compressed)

  return os.path.getsize(path + "/testC")

def getCSizeZip(file, path):
  with open(file, "rb") as in_file:
    compressed = zlip.compress(in_file.read(), 1)

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
  return (1 / (len(files) * (len(files) - 1))) * sumFiles

def setComplexityZip(files, path):
  sumFiles = 0
  for file1 in files:
    size1 = getCSizeZip(file1, path)
    for file2 in files:
      if file1 != file2:
        ncd = getNcdZip(file1, file2, path)
        sumFiles += size1 * ncd * (1 - ncd)
  return (1 / (len(files) * (len(files) - 1))) * sumFiles

def setComplexityBz2(files, path):
  sumFiles = 0
  for file1 in files:
    size1 = getCSizeBz2(file1, path)
    for file2 in files:
      if file1 != file2:
        ncd = getNcdBz2(file1, file2, path)
        sumFiles += size1 * ncd * (1 - ncd)
  return (1 / (len(files) * (len(files) - 1))) * sumFiles

def setComplexityPng(files, path):
  import math
  sumFiles = 0
  for file1 in files:
    size1 = os.path.getsize(file1)
    for file2 in files:
      if file1 != file2:
        ncd = getNcdPng(file1, file2, path)
        sumFiles += size1 * ncd * (1 - ncd)
  return (1 / (len(files) * (len(files) - 1))) * sumFiles

def setComplexity(files, path):
  return 1
  import math
  sumFiles = 0
  for file1 in files:
    size1 = getSizeGray(file1, path)
    for file2 in files:
      if file1 != file2:
        ncd = getNcdGray(file1, file2, path)
        sumFiles += size1 * ncd * (1 - ncd)
  return (1 / (len(files) * (len(files) - 1))) * sumFiles

if __name__ == "__main__":
  path = sys.argv[1]
  files = glob.glob(path + "/**/*.png")
  print(setComplexity(files, path))
