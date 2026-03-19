#!/usr/bin/python3
# Copyright 2010 Google Inc.
# Licensed under the Apache License, Version 2.0
# http://www.apache.org/licenses/LICENSE-2.0

# Google's Python Class
# http://code.google.com/edu/languages/google-python-class/

import os
import re
import sys
import urllib.request
import shutil

"""Logpuzzle exercise
Given an apache logfile, find the puzzle urls and download the images.

Here's what a puzzle url looks like:
10.254.254.28 - - [06/Aug/2007:00:13:48 -0700] "GET /~foo/puzzle-bar-aaab.jpg HTTP/1.0" 302 528 "-" "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.6) Gecko/20070725 Firefox/2.0.0.6"

"""
def sort_key(url):
  matches = re.search(r"\-[A-Za-z]{4}\-([A-Za-z]{4}).jpg$",url)
  if matches:
    return matches.group(1)
  return url

def read_urls(filename):
  """Returns a list of the puzzle urls from the given log file,
  extracting the hostname from the filename itself.
  Screens out duplicate urls and returns the urls sorted into
  increasing order."""
  # +++your code here+++
  pattern = r"GET (\S+) HTTP"
  url = set()
  if "_" in filename:
    idx = filename.index("_")
    server = filename[idx+1:]

  #if os.path.exists(f"logpuzzle/{filename}"):
  try:
    with open(f"{filename}","r",encoding= "utf-8") as file:
      for line in file:
        matches = re.search(pattern,line)
        if matches:
          if "puzzle" in matches.group(1):
            if server:
              full_url = "http://" + server + matches.group(1)
              url.add(full_url)
                      
      return sorted(url, key = sort_key)
  except Exception as e:
    print(f"Error occured: {e}")
    return []
          
    
def download_images(img_urls, dest_dir):
  """Given the urls already in the correct order, downloads
  each image into the given directory.
  Gives the images local filenames img0, img1, and so on.
  Creates an index.html in the directory
  with an img tag to show each local image file.
  Creates the directory if necessary.
  """
  index = 0
  # +++your code here+++
  try:
    if not os.path.exists(dest_dir):
      os.mkdir(dest_dir)
    for img in img_urls:   
      urllib.request.urlretrieve(img,f"{dest_dir}/img{index}")
      index += 1

    img_tags = "".join(f'<img src = "img{i}">'for i in range(index))
    with open(f"{dest_dir}/index.html","w") as file:
      file.write("<html>\n<body>\n")
      file.write(img_tags)
      file.write("\n</body>\n</html>")
        
  except Exception as e:
    print(f"Error in download_images {e}")

def main():
  args = sys.argv[1:]

  if not args:
    print('usage: [--todir dir] logfile ')
    sys.exit(1)

  todir = ''
  if args[0] == '--todir':
    todir = args[1]
    del args[0:2]

  img_urls = read_urls(args[0])

  if todir:
    download_images(img_urls, todir)
  else:
    print('\n'.join(img_urls))

if __name__ == '__main__':
  main()
