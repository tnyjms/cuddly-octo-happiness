#!/usr/local/bin/python2.7
# encoding: utf-8
'''
'''
from __future__ import print_function

import hashlib
import os
from argparse import ArgumentParser, RawDescriptionHelpFormatter
from operator import itemgetter

hasher = hashlib.sha256()

BLOCKSIZE = 65536

print 'Current directory : {0}'.format(os.path.realpath('.'))


class CLIError(Exception):
    '''Generic exception to raise and log different fatal errors.'''

    def __init__(self, msg):
        super(CLIError).__init__(type(self))
        self.msg = "E: %s" % msg

    def __str__(self):
        return self.msg

    def __unicode__(self):
        return self.msg


def main(argv=None):  # IGNORE:C0111
    '''Command line options.'''

    if argv is None:
        argv = sys.argv
    else:
        sys.argv.extend(argv)

    program_name = os.path.basename(sys.argv[0])
    program_version = "v%s" % __version__
    program_build_date = str(__updated__)
    program_version_message = '%%(prog)s %s (%s)' % (
        program_version, program_build_date)
    program_shortdesc = __import__('__main__').__doc__.split("\n")[1]
    program_license = '''%s

  Created by svt on %s.
  Copyright 2018 Cypress Semiconductor Ltd. All rights reserved.

USAGE
''' % (program_shortdesc, str(__date__))

    try:
        # Setup argument parser
        parser = ArgumentParser(
            description=program_license, formatter_class=RawDescriptionHelpFormatter)
        parser.add_argument("-p", "--path", dest="path",
                            help="WICED SDK or its complete path in either SMB or HTTP address [For example: %(default)s]", nargs='?', default=RELEASE_URL)
        parser.add_argument('--linux', action='append_const',
                            dest="os_", const='linux', help="Download SDK for LINUX")
        parser.add_argument('--win', action='append_const',
                            dest="os_", const='win', help="Download SDK for WINDOWS")
        parser.add_argument('--osx', action='append_const',
                            dest="os_", const='osx', help="Download SDK for OSX")
        parser.add_argument("--emlfile", dest="eml",
                            action='store_true', help="Downloads eml file with all options")
        parser.add_argument('-V', '--version', action='version',
                            version=program_version_message)

        # Process arguments
        args = parser.parse_args()
        path = args.path
        os_ = args.os_
        eml = args.eml
        sdk = ''

        if re.search(r'^\\samba', path):
            path = path.replace('\\', '/')
            path = path.replace('/samba', 'http://iot-webserver')
        if path.endswith('/'):
            path = path.rstrip('/')
        if path.split('/')[-3] == 'SW' and path.split('/')[-1] != '':
            sdk = path.split('/')[-1]
            path = '/'.join(path.split('/')[:-1])
        elif path.split('/')[-3] != 'Internal' or len(path.split('/')) != 8:
            print ('Invalid PATH : {}.\nUse "" to escape slash \\\n'.format(path))
            raise ValueError
        if sdk == '':
            sdk = get_latest_sdk()
        if os_ is None:
            os_ = ['win']
        print ('Downloading SDK...')
        print ('SDK Path    : {}'.format(path))
        print ('SDK         : {}'.format(sdk))
        print ('OS          : {}'.format(os_))
        print ('EML Config  : {}'.format(eml))
        for i in os_:
            wget.download(get_sdk_filename(sdk, os_=i, path=path))
        if eml:
            wget.download(get_config(sdk, path))
    except KeyboardInterrupt:
        # handle keyboard interrupt
        return 0
    except Exception, e:
        if DEBUG or TESTRUN:
            raise(e)
        indent = len(program_name) * " "
        sys.stderr.write(program_name + ": " + repr(e) + "\n")
        sys.stderr.write(indent + "  for help use --help\n")
        parser.print_help()
        return 2


if __name__ == "__main__":
    if DEBUG:
        sys.argv.append("-h")
        sys.argv.append("-v")
    if TESTRUN:
        import doctest
        doctest.testmod()
    if PROFILE:
        import cProfile
        import pstats
        profile_filename = 'src.apps.sample_profile.txt'
        cProfile.run('main()', profile_filename)
        statsfile = open("profile_stats.txt", "wb")
        p = pstats.Stats(profile_filename, stream=statsfile)
        stats = p.strip_dirs().sort_stats('cumulative')
        stats.print_stats()
        statsfile.close()
        sys.exit(0)
    sys.exit(main())

# for dirpath, dirnames, files in os.walk('.'):
#     if files is not None:
#         for name in files:
#             ext = name.lower().rsplit('.', 1)[-1]
#             if ext in ['bin', 'cfg']:
#                 with open(os.path.join(dirpath, name), 'rb') as afile:
#                     buf = afile.read(BLOCKSIZE)
#                     while len(buf) > 0:
#                         hasher.update(buf)
#                         buf = afile.read(BLOCKSIZE)
#                 if hasher.hexdigest() not in d.keys():
#                     d[hasher.hexdigest()] = os.path.join(dirpath, name)
#                 else:
#                     print "Error: Duplicate found"
#                     print "Duplicate files are :\n\t{0}\n\t{1}".format(
#                         d[hasher.hexdigest()], name)
#                     flag = 1
# if flag == 0:
#     print "\n\nSuccess - No duplicates found for {0} items".format(len(d))
#     print "\n\nDebug \n---------------------------\n"
#     for k, v in d.iteritems():
#         print "File : %64s, SHA1 Hash : %40s" % (str(v.split('\\')[-1]), k)
