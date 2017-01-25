#!/usr/bin/python
"""
Created on Jan 23, 2017
@author: SAW111
"""
import os, re, sys
import csv

levelsFromRootDirToCountryDirs = 0
recordTypes = ['people', 'household']
skippedDirs = ['input', 'diags', 'logfiles']

def toRecordType(path):
    for type in recordTypes:
        key = '/' + type + '_'
        if re.search(key, path) and path.endswith(('.csv')):
            return type
    return 'unknown'


def head(path):
    with open(path, 'r') as f:
        return f.readline().rstrip()


def handle(src, dst):
    print dst
    #os.mknod(dst)
    with open(src, 'rt') as fp:
        reader = csv.DictReader(fp)
        map = {}
        for row in reader:
            for key in row.keys():
                if key not in map:
                    map[key] = {}
                data_map = map[key]
                data = row[key]
                if data not in data_map:
                    data_map[data] = 0 + 1
                else:
                    data_map[data] += 1
        for key in map.keys():
            filename = dst + '.' + key + '.csv'
            dict = map[key]
            save(filename, dict)


def save(filename, dict):
    print filename
    with open(filename, 'w') as csvfile:
        fieldnames = dict.keys()
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerow(dict)
################################################################################
def walk(src, dst, level):
    try:
        files = os.listdir(src)
        for fileName in files:
            srcPath = src + "/" + fileName
            try:
                if os.path.isdir(srcPath):
                    if fileName in skippedDirs:
                        continue
                    dstPath = dst
                    if level >= levelsFromRootDirToCountryDirs - 1:
                        dstPath += "/" + fileName
                        # print dstPath
                        if (not os.path.exists(dstPath)):
                            os.makedirs(dstPath)
                    walk(srcPath, dstPath, level + 1)
                else:
                    dstPath = dst + "/" + fileName
                    if toRecordType(srcPath) != 'unknown':
                        handle(srcPath, dstPath)
                   
            except:
                print srcPath, ": unexpected error:", sys.exc_info()[0]
    except:
        print src, ": Unexpected error:", sys.exc_info()[0]

################################################################################
def main(args):
    walk('in_data', 'out_data', 0)
    
if __name__ == "__main__":
    #import sys
    main(sys.argv)
