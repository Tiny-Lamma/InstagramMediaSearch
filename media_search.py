#!/usr/bin/python
# -*- coding: utf-8 -*-
import os

def write_file(filename, content):
    f = open(filename, "w+")
    for line in content:
        f.write(line)
    f.close()

def is_mp4(filename):
    data = open(filename,'rb').read(8)  # read first 11 bytes
    if data == b'\x00\x00\x00$ftyp':  # mp4 magic header
        return '<video width="320" height="240" controls><source src="{0}" type="video/mp4"></video>\n'.format(filename)  # mp4 html output
    return ''
    
def is_jpg(filename):
    data = open(filename,'rb').read(11)  # read first 11 bytes
    if data[:4] == b'\xff\xd8\xff\xe0' and data[6:] == b'JFIF\x00':  # jpg magic header
        return'<img src="{0}">\n'.format(filename)  # jpg html output
    return ''
    
def main():
    mp4Files = list()
    jpgFiles = list()
    
    folderName = r'0770F46B-A42B-4400-9FA7-EB48DF0EBC75'  # instagram data folder name

    # get complete filelist
    fileList = list()
    for (dirpath, dirnames, filenames) in os.walk(folderName):
        fileList += [os.path.join(dirpath, file) for file in filenames]

    for file in fileList:
        mp4Files += is_mp4(file)  # filename returned if file is mp4 format
        jpgFiles += is_jpg(file)  # filename returned if file is jpg format
    
    # output all media, split into videos or photos
    write_file('videos.html', mp4Files)
    write_file('images.html', jpgFiles)

if __name__ == "__main__":
    main()
