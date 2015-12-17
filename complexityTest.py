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

import setComplexity

if __name__ == "__main__":
  import shutil
  complexityList = []
  path = sys.argv[1]

  best1 = 0
  best2 = 0
  best3 = 0
  best4 = 0
  best5 = 0
  testoutput = open(path + "/complexityTest.txt", "w")

  iteration = 0
  files = glob.glob(path + "/" + str(iteration) + "-*/*.png")
  while len(files) > 0:
    files.sort(key=os.path.getmtime)
    print(files)
    #complexity1 = setComplexity.setComplexityPng(files, path)
    #complexity2 = setComplexity.setComplexityBz2(files, path)
    #complexity3 = setComplexity.setComplexityJpeg(files, path)
    #complexity4 = setComplexity.setComplexitySimple(files, path)
    complexity5 = setComplexity.setComplexity(files, path)
    #if (complexity1 > best1):
    #  best1 = complexity1
    #  shutil.copyfile(files[0], path + "/BestPngTest.png")
    #if (complexity2 > best2):
    #  best2 = complexity2
    #  shutil.copyfile(files[0], path + "/BestBz2Test.png")
    #if (complexity3 > best3):
    #  best3 = complexity3
    #  shutil.copyfile(files[0], path + "/BestJpegTest.png")
    #if (complexity4 > best4):
    #  best4 = complexity4
    #  shutil.copyfile(files[0], path + "/BestSimpleTest.png")
    if (complexity5 > best5):
      best5 = complexity5
      shutil.copyfile(files[0], path + "/BestGrayTest.png")
    testoutput.writelines(str(complexity5) + "\n")

    iteration += 1
    files = glob.glob(path + "/" + str(iteration) + "-*/*.png")

