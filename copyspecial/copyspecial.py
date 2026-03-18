#!/usr/bin/python3
# Copyright 2010 Google Inc.
# Licensed under the Apache License, Version 2.0
# http://www.apache.org/licenses/LICENSE-2.0

# Google's Python Class
# http://code.google.com/edu/languages/google-python-class/

import sys
import re
import os
import shutil
import subprocess
from zipfile import ZipFile

"""Copy Special exercise
"""

# +++your code here+++
# Write functions and modify main() to call them

def get_special_paths(dir):
  try:
    dir_list = os.listdir(dir)# This returns a list.
    pattern = re.compile(r"__\w+__")
    matched = []
    for s in dir_list:
      if pattern.search(s):
        joined = os.path.join(dir,s)
        matched.append(os.path.abspath(joined))
    
    return matched
  except FileNotFoundError:
    return f"Directory {dir} does not exist."

def copy_to(source_path,dest_path):
  if not os.path.exists(dest_path):
    os.makedirs(dest_path)
  shutil.copy(source_path,dest_path)

def zip_to(source_path,zip_path):
  #the cmd command will look like zip -j zipfile path1 path2 path3 ...
  with ZipFile(zip_path,'w')as myzip:
    for p in source_path:
      #use w not x cause w is safer for if it already exists
      myzip.write(p, arcname=os.path.basename(p))
      #without the arcname parameter it creates a zip of the whole path but we only need for the last file/folder
    
def main():
  # This basic command line argument parsing code is provided.
  # Add code to call your functions below.

  # Make a list of command line arguments, omitting the [0] element
  # which is the script itself.
  args = sys.argv[1:]
  if not args:
    print('usage: [--todir dir][--tozip zipfile] dir [dir ...]')
    sys.exit(1)

  # todir and tozip are either set from command line
  # or left as the empty string.
  # The args array is left just containing the dirs.
  todir = ''
  #this copies the special file into the folder that comes after --todir
  if args[0] == '--todir':
    todir = args[1]
    del args[0:2]

  tozip = ''
  #zip the special files into this zipfile
  if args[0] == '--tozip':
    tozip = args[1]
    del args[0:2]

  if not args: # A zero length array evaluates to "False".
    print('error: must specify one or more dirs')
    sys.exit(1)

  # +++your code here+++
  # Call your functions
  all_paths = []
  for d in  args:
    all_paths.extend(get_special_paths(d))

  if todir:
    for i in all_paths:
      copy_to(i,todir)
    print("Files copied.")
  elif tozip:
    zip_to(all_paths,tozip)
    print('Zip file created')
  else:
    print(*all_paths,sep ='\n') #prints each item on a new line  
if __name__ == '__main__':
  main()
