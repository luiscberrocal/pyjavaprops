-------------
pyjavaprops
-------------

.. image:: https://travis-ci.org/luiscberrocal/pyjavaprops.svg?branch=master
    :target: https://travis-ci.org/luiscberrocal/pyjavaprops

.. image:: https://coveralls.io/repos/luiscberrocal/pyjavaprops/badge.svg?branch=master&service=github
    :target: https://coveralls.io/github/luiscberrocal/pyjavaprops?branch=master

.. image:: https://badge.fury.io/py/pyjavaprops.svg
    :target: http://badge.fury.io/py/pyjavaprops


Library to read Java style properties files. I don't particularly like properties files but working with them in Java
is very easy. I recently had to support reading Java properties files using Python.

This project is based on Benjamins Brent fork of pyjavaproperties_.

The libraries main features are:

- Reads properties files.

- You can add new properties.

- You can save properties to file.

- It interprets variables in curly braces {} and dollar curly braces ${}.

.. _pyjavaproperties: https://bitbucket.org/benjaminbrent/pyjavaproperties-python3

Caveats
--------

The library does not interpret unicode characters correctly. If you include charactes like \u4500 it will interpret it
as \, letter y and the number 4500.


Installation
--------------

Requires Python 3.3 or better. 

.. code-block:: console

    $ pip install pyjavaprops
    
Usage
------


Loading Java properties
=========================

.. code-block:: python

    filename = os.path.join(TEST_DATA_FOLDER, 'iso-8859-1.properties')
    iso_8859_1_properties = JavaProperties()
    with open(filename, encoding='iso-8859-1') as property_file:
        iso_8859_1_properties.load(property_file)
         name = iso_8859_1_properties['name']

Saving Java properties to file
================================

.. code-block:: python

    filename = os.path.join(TEST_DATA_FOLDER, 'simple.properties')
    simple_java_properties = JavaProperties()
    with open(filename) as property_file:
        simple_java_properties.load(property_file)
    simple_java_properties['country'] = 'Angola'
    output_filename = os.path.join(OUTPUT_FOLDER, 'simple_%s.properties' % datetime.now().strftime('%Y%m%d_%H%M'))
    with open(output_filename, mode='w') as output:
        simple_java_properties.store(output)

Exporting to json
===================


.. code-block:: python

    output_filename = os.path.join(OUTPUT_FOLDER, 'simple_%s.json' % datetime.now().strftime('%Y%m%d_%H%M'))
    export_to_json(output_filename, java_properties)
    with open(output_filename) as json_data:
        json_properties = json.load(json_data)
        print(json_properties['Key10'])




Development
------------


Virtual Environment
====================


To create the virtual environment

.. code-block:: bash

    $ cd ~/virtual_environments

    $ python3 /usr/local/lib/python3.4/site-packages/virtualenv.py --no-site-packages pyjavaprops_env

    $ source ./pyjavaprops_env/bin/activate

    (pyjavaprops_env) $


Runnig Tests
=============

.. code-block:: bash

    $ coverage run --source pyjavaprops setup.py test
