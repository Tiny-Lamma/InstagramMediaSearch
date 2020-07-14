#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import sqlite3

from bplist import bplist
from sqlite3 import Error


def write_file(filename, content):
    with open(filename, "w+", encoding="utf-8") as f:
        for line in content:
            f.write(line)
        f.close()


def is_mp4(filename):
    data = open(filename, 'rb').read(8)  # read first 11 bytes
    if data == b'\x00\x00\x00$ftyp':  # mp4 magic header
        return '<video width="320" height="240" controls><source src="{0}" type="video/mp4"></video>\n'.format(
            filename)  # mp4 html output
    return ''


def is_jpg(filename):
    data = open(filename, 'rb').read(11)  # read first 11 bytes
    if data[:4] == b'\xff\xd8\xff\xe0' and data[6:] == b'JFIF\x00':  # jpg magic header
        return '<img src="{0}">\n'.format(filename)  # jpg html output
    return ''


def is_message(filename, message):
    if filename[-3:] == '.db':
        data = open(filename, 'rb').read()
        if message.encode('utf-8') in data:
            return True
    return False


def bplist_message(data):
    parsed = bplist.BPListReader(data).parse()
    message = parsed['$objects'][11]  # doesn't appear to be perfect.
    if message:
        if type(message) == bytes:
            return message.decode('utf-8') + '<br>'
        elif type(message) == str:
            return message + '<br>'
        elif type(message) == dict:
            return '<br><br>'
        else:
            return '<br></br>'


def get_messages(message_files):
    messages = list()
    for db in message_files:
        connection = create_connection(db)
        if connection:
            query = 'SELECT archive FROM messages;'
            messages += db_query(connection, query)

            # output all media, split into videos or photos
    return messages


def create_connection(db_file):
    connection = None
    try:
        connection = sqlite3.connect(db_file)
    except Error as e:
        print(e)

    return connection


def db_query(connection, query):
    cursor = connection.cursor()
    cursor.execute(query)

    rows = cursor.fetchall()

    data = list()

    for row in rows:
        for line in row:
            data += bplist_message(line)
    return data


def main():
    mp4_files = list()
    jpg_files = list()
    message_files = list()

    dir_path = os.path.dirname(os.path.realpath(__file__))
    folder_name = \
        r'\0770F46B-A42B-4400-9FA7-EB48DF0EBC75'  # Instagram data folder name

    # get complete file listing
    file_list = list()
    for (dirpath, dirnames, filenames) in os.walk(dir_path+folder_name):
        file_list += [os.path.join(dirpath, file) for file in filenames]

    message_search_term = 'IGDirectPublishedMessageMetadata'

    for file in file_list:
        mp4_files.append(is_mp4(file))  # html display code is returned if file is mp4 format.
        jpg_files.append(is_jpg(file))  # html display code is returned if file is jpg format.
        if is_message(file, message_search_term):
            message_files.append(file)

    messages = get_messages(message_files)
    write_file('videos.html', mp4_files)
    write_file('images.html', jpg_files)
    write_file('messages.html', messages)


if __name__ == '__main__':
    main()
