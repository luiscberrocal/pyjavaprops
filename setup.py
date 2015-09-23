from setuptools import setup, find_packages

setup(
    name='pyjavaprops',
    version='0.1.0',
    description='Tool parse Java style properties file',
    author='Luis Carlos Berrocal',
    author_email ='luis.berrocal.1942@gmail.com',
    packages=find_packages(),
    url='https://github.com/luiscberrocal/pyjavaprops',
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
        'console_scripts': [],
    }
)