#!/usr/bin/env python
'''
Demo for SAR parser.
'''

import os
import sys
import pprint


def main():
    from sar import parser

    sysstat_dir = '/var/log/sa'
    single_file = ('%s/%s' % (sysstat_dir, 'sar05'))

    # Single SAR file parsing
    insar = parser.Parser(single_file)
    print(("SAR file date: %s" % (insar.get_filedate())))
    print("Content:\n")
    pprint.pprint(insar.get_sar_info())

    print(("-" * 78))

    # Id you want to test his, please run something like
    #  $ cat /var/log/sa/sar* > sarcombined
    # to create "combined" SAR file. Then uncomment the following:
    '''
    from sar import multiparser
    multi_file = ('./%s' % ('sarcombined'))
    inmulti = multiparser.Multiparser(multi_file)
    inmulti.load_file()
    print("Content:\n")
    pprint.pprint(inmulti.get_sar_info())
    '''


def set_include_path():
    include_path = os.path.abspath("./")
    sys.path.append(include_path)


if __name__ == "__main__":
    set_include_path()
    main()
