import json
import os
from pyjavaprops.javaproperties import JavaProperties, export_to_json
from pyjavaprops.settings.test import TEST_DATA_FOLDER, OUTPUT_FOLDER
from datetime import datetime

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

    def test_get_names(self):
        #Key16\ With\ Spaces:Value16
        self.assertEqual(25, len(self.java_properties.property_names()))

    def test_load(self):
        filename = os.path.join(TEST_DATA_FOLDER, 'simple.properties')
        simple_java_properties = JavaProperties()
        simple_java_properties.load(open(filename))
        self.assertEqual('1.5, 1.6.1, 1.7, 1.8,', simple_java_properties['supported.java.versions'])

    def test_load_windows_1252(self):
        filename = os.path.join(TEST_DATA_FOLDER, 'windows-1252.properties')
        simple_java_properties = JavaProperties()
        simple_java_properties.load(open(filename, encoding='windows-1252'))
        name = simple_java_properties['name']
        self.assertEqual('Rodríguez', name)

    def test_load_iso_8859_1(self):
        filename = os.path.join(TEST_DATA_FOLDER, 'iso-8859-1.properties')
        iso_8859_1_properties = JavaProperties()
        with open(filename, encoding='iso-8859-1') as property_file:
            iso_8859_1_properties.load(property_file)
            name = iso_8859_1_properties['name']
            self.assertEqual('Rodríguez', name)
            country = iso_8859_1_properties['país']
            self.assertEqual('Panamá', country)

    def test_store(self):
        filename = os.path.join(TEST_DATA_FOLDER, 'simple.properties')
        simple_java_properties = JavaProperties()
        with open(filename) as property_file:
            simple_java_properties.load(property_file)
        simple_java_properties['country'] = 'Angola'
        output_filename = os.path.join(OUTPUT_FOLDER, 'simple_%s.properties' % datetime.now().strftime('%Y%m%d_%H%M'))
        with open(output_filename, mode='w') as output:
            simple_java_properties.store(output)

        with open(output_filename) as property_file:
            simple_java_properties.load(property_file)

        self.assertEqual('Angola', simple_java_properties['country'])

    def test_json_adapter(self):
        output_filename = os.path.join(OUTPUT_FOLDER, 'simple_%s.json' % datetime.now().strftime('%Y%m%d_%H%M'))
        export_to_json(output_filename, self.java_properties)
        with open(output_filename) as json_data:
            json_properties = json.load(json_data)
        self.assertEqual('Value10', json_properties['Key10'])


if __name__ == '__main__':
    unittest.main()
