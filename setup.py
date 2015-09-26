from setuptools import setup, find_packages

with open("README.rst") as src:
    readme = src.read()

version = '1.0.1'

setup(
    name='pyjavaprops',
    version=version,
    description='Tool to parse Java style properties file',
    long_description=readme,
    author='Luis Carlos Berrocal',
    author_email ='luis.berrocal.1942@gmail.com',
    packages=find_packages(),
    url='https://github.com/luiscberrocal/pyjavaprops',
    download_url = 'https://github.com/luiscberrocal/pyjavaprops/archive/v%s.zip' % version,
    license='MIT',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.4',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: User Interfaces',
        'Topic :: Terminals'
    ],
    install_requires=[
    ],
    entry_points = {
        'console_scripts': ['list-settings=pyjavaprops.settings.base:main'],
    },
    test_suite="tests",
)