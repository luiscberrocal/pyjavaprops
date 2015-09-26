#! /usr/bin/env python

"""
A Python replacement for java.util.Properties class
This is modelled as closely as possible to the Java original.

Created - Anand B Pillai <abpillai@gmail.com>
"""
from __future__ import print_function
import json
import os
import io
import sys
import re
import time


IS_PY3 = sys.version_info[0] == 3


def export_to_json(filename, java_properties, encoding='utf-8'):
    with open(filename, 'w', encoding=encoding) as outfile:
        json.dump(java_properties.get_property_dict(), outfile, indent=4)


class IllegalArgumentException(Exception):

    def __init__(self, lineno, msg):
        self.lineno = lineno
        self.msg = msg

    def __str__(self):
        s='Exception at line number %d => %s' % (self.lineno, self.msg)
        return s


class JavaProperties(object):
    """ A Python replacement for java.util.Properties """

    def __init__(self, props=None):

        # Note: We don't take a default properties object
        # as argument yet

        # Dictionary of properties.
        self._properties = {}
        # Dictionary of properties with 'pristine' keys
        # This is used for dumping the properties to a file
        # using the 'store' method
        self._origprops = {}
        self._keyorder = []
        # Dictionary mapping keys from property
        # dictionary to pristine dictionary
        self._keymap = {}

        self.othercharre = re.compile(r'(?<!\\)(\s*\=)|(?<!\\)(\s*\:)')
        self.othercharre2 = re.compile(r'(\s*\=)|(\s*\:)')
        self.bspacere = re.compile(r'\\(?!\s$)')

    def __str__(self):
        s='{'
        for key,value in self._properties.items():
            s = ''.join((s,key,'=',value,', '))

        s=''.join((s[:-2],'}'))
        return s

    def __parse(self, lines):
        """ Parse a list of lines and create
        an internal property dictionary """

        # Every line in the file must consist of either a comment
        # or a key-value pair. A key-value pair is a line consisting
        # of a key which is a combination of non-white space characters
        # The separator character between key-value pairs is a '=',
        # ':' or a whitespace character not including the newline.
        # If the '=' or ':' characters are found, in the line, even
        # keys containing whitespace chars are allowed.

        # A line with only a key according to the rules above is also
        # fine. In such case, the value is considered as the empty string.
        # In order to include characters '=' or ':' in a key or value,
        # they have to be properly escaped using the backslash character.

        # Some examples of valid key-value pairs:
        #
        # key     value
        # key=value
        # key:value
        # key     value1,value2,value3
        # key     value1,value2,value3 \
        #         value4, value5
        # key
        # This key= this value
        # key = value1 value2 value3

        # Any line that starts with a '#' or '!' is considerered a comment
        # and skipped. Also any trailing or preceding whitespaces
        # are removed from the key/value.

        # This is a line parser. It parses the
        # contents like by line.

        lineno=0
        i = iter(lines)

        for line in i:
            lineno += 1
            line = line.strip()
            # Skip null lines
            if not line: continue
            # Skip lines which are comments
            if line[0] in ('#','!'): continue
            # Some flags
            escaped=False
            # Position of first separation char
            sepidx = -1
            # A flag for performing wspace re check
            flag = 0
            # Check for valid space separation
            # First obtain the max index to which we
            # can search.
            m = self.othercharre.search(line)
            if m:
                first, last = m.span()
                start, end = 0, first
                flag = 1
                wspacere = re.compile(r'(?<![\\\=\:])(\s)')
            else:
                if self.othercharre2.search(line):
                    # Check if either '=' or ':' is present
                    # in the line. If they are then it means
                    # they are preceded by a backslash.

                    # This means, we need to modify the
                    # wspacere a bit, not to look for
                    # : or = characters.
                    wspacere = re.compile(r'(?<![\\])(\s)')
                start, end = 0, len(line)

            m2 = wspacere.search(line, start, end)
            if m2:
                # print 'Space match=>',line
                # Means we need to split by space.
                first, last = m2.span()
                sepidx = first
            elif m:
                # print 'Other match=>',line
                # No matching wspace char found, need
                # to split by either '=' or ':'
                first, last = m.span()
                sepidx = last - 1
                # print line[sepidx]


            # If the last character is a backslash
            # it has to be preceded by a space in which
            # case the next line is read as part of the
            # same property
            while line[-1] == '\\':
                # Read next line
                nextline = next(i)
                nextline = nextline.strip()
                lineno += 1
                # This line will become part of the value
                line = line[:-1] + nextline

            # Now split to key,value according to separation char
            if sepidx != -1:
                key, value = line[:sepidx], line[sepidx+1:]
            else:
                key,value = line,''
            self._keyorder.append(key)
            self.process_pair(key, value)

    def process_pair(self, key, value):
        """ Process a (key, value) pair """

        old_key = key
        old_value = value

        # Create key intelligently
        keyparts = self.bspacere.split(key)
        # print keyparts

        strippable = False
        lastpart = keyparts[-1]

        if lastpart.find('\\ ') != -1:
            keyparts[-1] = lastpart.replace('\\','')

        # If no backspace is found at the end, but empty
        # space is found, strip it
        elif lastpart and lastpart[-1] == ' ':
            strippable = True

        key = ''.join(keyparts)
        if strippable:
            key = key.strip()
            old_key = old_key.strip()

        old_value = self.unescape(old_value)
        value = self.unescape(value)

        # Patch from N B @ ActiveState
        curlies = re.compile(r'\$?\{.+?\}')
        found_variables = curlies.findall(value)

        for found_variable in found_variables:
            if found_variable.startswith('$'):
                source_key = found_variable[2:-1]
            else:
                source_key = found_variable[1:-1]

            if source_key in self._properties:
                value = value.replace(found_variable, self._properties[source_key], 1)

        self._properties[key] = value.strip()

        # Check if an entry exists in pristine keys
        if key in self._keymap:
            old_key = self._keymap.get(key)
            self._origprops[old_key] = old_value.strip()
        else:
            self._origprops[old_key] = old_value.strip()
            # Store entry in keymap
            self._keymap[key] = old_key

        if key not in self._keyorder:
            self._keyorder.append(key)

    def escape(self, value):

        # Java escapes the '=' and ':' in the value
        # string with backslashes in the store method.
        # So let us do the same.
        newvalue = value.replace(':','\:')
        newvalue = newvalue.replace('=','\=')

        return newvalue

    def unescape(self, value):

        # Reverse of escape
        newvalue = value.replace('\:',':')
        newvalue = newvalue.replace('\=','=')

        return newvalue

    def load(self, stream):
        """ Load properties from an open file stream """

        # For the time being only accept file input streams
        if not _is_file(stream):
            raise TypeError('Argument should be a file object!')
        # Check for the opened mode
        if stream.mode != 'r':
            raise ValueError('Stream should be opened in read-only mode!')

        try:
            lines = stream.readlines()
            self.__parse(lines)
        except IOError:
            raise

    def get_property(self, key):
        """ Return a property for the given key """

        return self._properties.get(key,'')

    def set_property(self, key, value):
        """ Set the property for the given key """

        if type(key) is str and type(value) is str:
            self.process_pair(key, value)
        else:
            raise TypeError('Both key and value should be strings!')

    def property_names(self):
        """ Return an iterator over all the keys of the property
        dictionary, i.e the names of the properties """

        return self._properties.keys()

    def list(self, out=sys.stdout):
        """ Prints a listing of the properties to the
        stream 'out' which defaults to the standard output """

        out.write('-- listing properties --\n')
        for key,value in self._properties.items():
            out.write(''.join((key,'=',value,'\n')))

    def store(self, out, header=""):
        """ Write the properties list to the stream 'out' along
        with the optional 'header' """

        if out.mode[0] != 'w':
            raise ValueError('Steam should be opened in write mode!')

        try:
            out.write(''.join(('#',header,'\n')))
            # Write timestamp
            tstamp = time.strftime('%a %b %d %H:%M:%S %Z %Y', time.localtime())
            out.write(''.join(('#',tstamp,'\n')))
            # Write properties from the pristine dictionary
            for prop in self._keyorder:
                if prop in self._origprops:
                    val = self._origprops[prop]
                    out.write(''.join((prop,'=',self.escape(val),'\n')))

            out.close()
        except IOError:
            raise

    def get_property_dict(self):
        return self._properties

    def __getitem__(self, name):
        """ To support direct dictionary like access """

        return self.get_property(name)

    def __setitem__(self, name, value):
        """ To support direct dictionary like access """

        self.set_property(name, value)

    def __getattr__(self, name):
        """ For attributes not found in self, redirect
        to the properties dictionary """

        try:
            return self.__dict__[name]
        except KeyError:
            if hasattr(self._properties,name):
                return getattr(self._properties, name)


def _is_file(obj):
    if not IS_PY3:
        return isinstance(obj, file)
    return isinstance(obj, io.IOBase)


if __name__=="__main__":
    p = JavaProperties()
    p.load(open('test2.properties'))
    p.list()
    print(p)
    print(p.items())
    print(p['name3'])
    p['name3'] = 'changed = value'
    print(p['name3'])
    p['new key'] = 'new value'
    p.store(open('test2.properties','w'))
