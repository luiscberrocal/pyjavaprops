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
is very easy. I recently had to support reading properties files using Python.

This project is based on Benjamins Brent fork of pyjavaproperties_.

.. _pyjavaproperties: https://bitbucket.org/benjaminbrent/pyjavaproperties-python3

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
