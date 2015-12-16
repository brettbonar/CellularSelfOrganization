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

if __name__ == "__main__":
  import shutil
  path = sys.argv[1]
  #print(path)
  files = glob.glob(path + "/**/*.png")
  #print(files)
  files.sort(key=os.path.getmtime)

  it = 0
  firstfiles = files[0::4]
  for file in firstfiles:
    shutil.copyfile(file, path + "/Sequence/" + str(it) + ".png")
    it += 1
