#!/usr/local/bin/python2.7
# encoding: utf-8
'''
'''
from __future__ import print_function

import hashlib
import os

hasher = hashlib.sha256()

BLOCKSIZE = 65536

print 'Current directory : {0}'.format(os.path.realpath('.'))


if __name__ == "__main__":
    sys.exit

for dirpath, dirnames, files in os.walk('.'):
    if files is not None:
        for name in files:
            ext = name.lower().rsplit('.', 1)[-1]
            if ext in ['bin', 'cfg']:
                with open(os.path.join(dirpath, name), 'rb') as afile:
                    buf = afile.read(BLOCKSIZE)
                    while len(buf) > 0:
                        hasher.update(buf)
                        buf = afile.read(BLOCKSIZE)
                if hasher.hexdigest() not in d.keys():
                    d[hasher.hexdigest()] = os.path.join(dirpath, name)
                else:
                    print "Error: Duplicate found"
                    print "Duplicate files are :\n\t{0}\n\t{1}".format(
                        d[hasher.hexdigest()], name)
                    flag = 1
if flag == 0:
    print "\n\nSuccess - No duplicates found for {0} items".format(len(d))
    print "\n\nDebug \n---------------------------\n"
    for k, v in d.iteritems():
        print "File : %64s, SHA1 Hash : %40s" % (str(v.split('\\')[-1]), k)
