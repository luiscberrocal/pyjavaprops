import os
from pyjavaprops.settings.base import *
__author__ = 'luiscberrocal'


TEST_DATA_FOLDER = os.path.abspath(os.path.join(APP_ROOT, '..', 'testdata'))

OUTPUT_FOLDER = os.path.abspath(os.path.join(APP_ROOT, '..', 'output'))


if not os.path.exists(OUTPUT_FOLDER):
    os.makedirs(OUTPUT_FOLDER)