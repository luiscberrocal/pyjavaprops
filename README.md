# pyjavaprops

Library to read Java style properties files. I don't particularly like properties files but working with them in Java
is very easy. I recently had to support reading properties files using Python.

This project is based on Benjamins Brent fork of pyjavaproperties https://bitbucket.org/benjaminbrent/pyjavaproperties-python3

## Installation

Requires Python3. 

    $ pip install pyjavaprops
    
# Usage

    filename = os.path.join(TEST_DATA_FOLDER, 'complex.properties')
    java_properties = JavaProperties()
    java_properties.load(open(filename))
    
    print(java_properties['Key14'])

## Development

To create the virtual environment

    $ cd ~/virtual_environments

    $ python3 /usr/local/lib/python3.4/site-packages/virtualenv.py --no-site-packages pyjavaprops_env

    $ source ./pyjavaprops_env/bin/activate

    (pyjavaprops_env) $

