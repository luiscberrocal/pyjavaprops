from setuptools import setup, find_packages

version = '0.1.2'
setup(
    name='pyjavaprops',
    version=version,
    description='Tool parse Java style properties file',
    author='Luis Carlos Berrocal',
    author_email ='luis.berrocal.1942@gmail.com',
    packages=find_packages(),
    url='https://github.com/luiscberrocal/pyjavaprops',
    download_url = 'https://github.com/luiscberrocal/pyjavaprops/tarball/v%s' % version,
    license='MIT',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.4',
    ],
    install_requires=[
    ],
    entry_points = {
        'console_scripts': ['list-settings=pyjavaprops.settings.base:main'],
    }
)