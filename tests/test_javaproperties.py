import os
from pyjavaprops.javaproperties import JavaProperties
from pyjavaprops.settings.test import TEST_DATA_FOLDER

__author__ = 'luiscberrocal'

import unittest


class JavaPropertiesTestCase(unittest.TestCase):

    def setUp(self):
        filename = os.path.join(TEST_DATA_FOLDER, 'complex.properties')
        self.java_properties = JavaProperties()
        self.java_properties.load(open(filename))

    def test_value_with_spaces(self):
        self.assertEqual('Value14 With Spaces', self.java_properties['Key14'])
        self.assertEqual('Value01-test', self.java_properties['Key23'])

    def test_variable(self):
        self.assertEqual('Value01-test', self.java_properties['Key23'])

    def test_variable_dollar(self):
        self.assertEqual('Value01/path/to/myapp', self.java_properties['Key24'])

    def test_key_with_spaces_eq(self):
        #Key17\ With\ Spaces=Value17
        self.assertEqual('Value17', self.java_properties['Key17 With Spaces'])

    def test_key_with_spaces(self):
        #Key16\ With\ Spaces:Value16
        self.assertEqual('Value16', self.java_properties['Key16 With Spaces'])

    def test_load(self):
        filename = os.path.join(TEST_DATA_FOLDER, 'simple.properties')
        simple_java_properties = JavaProperties()
        simple_java_properties.load(open(filename))
        self.assertEqual('1.5, 1.6.1, 1.7, 1.8,', simple_java_properties['supported.java.versions'])


if __name__ == '__main__':
    unittest.main()
