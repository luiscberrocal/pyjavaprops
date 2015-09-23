import os
from pyjavaprops.javaproperties import Properties
from pyjavaprops.settings.test import TEST_DATA_FOLDER

__author__ = 'luiscberrocal'

import unittest


class JavaPropertiesTestCase(unittest.TestCase):
    def test_load(self):
        filename = os.path.join(TEST_DATA_FOLDER, 'complex.properties')
        p = Properties()
        p.load(open(filename))
        self.assertEqual('Value14 With Spaces', p['Key14'])


if __name__ == '__main__':
    unittest.main()
