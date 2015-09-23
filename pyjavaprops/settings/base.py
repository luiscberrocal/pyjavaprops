from os.path import dirname, abspath, basename
import collections
import re

__author__ = 'luiscberrocal'

APP_ROOT = dirname(dirname(abspath(__file__)))
SITE_NAME = basename(APP_ROOT)

def print_constants(vars_dict):
    od = collections.OrderedDict(sorted(vars_dict.items()))
    for var, value in od.items():
        regexp = '^[A-Z][A-Z_]+'
        match = re.search(regexp, var)
        if match:
            print('%-35s : %r' % (var, value))

def main():
    print_constants(globals())

if __name__ == '__main__':
    main()
