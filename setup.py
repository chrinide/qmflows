#!/usr/bin/env python

from setuptools import setup


def readme():
    with open('README.rst') as f:
        return f.read()


setup(
    name='qmflows',
    version='0.4.0',
    description='Automation of computations in quantum chemistry',
    license='Apache 2.0',
    url='https://github.com/SCM-NV/qmflows',
    author=['Felipe Zapata'],
    author_email='f.zapata@esciencecenter.nl',
    keywords='chemistry workflows simulation materials',
    long_description=readme(),
    package_dir={'': 'src'},
    packages=["qmflows",
              "qmflows.components",
              "qmflows.data",
              "qmflows.data.dictionaries",
              "qmflows.examples",
              "qmflows.examples.Conditional_workflows",
              "qmflows.examples.Constrained_and_TS_optimizations",
              "qmflows.examples.FDE_Fragments",
              "qmflows.hdf5",
              "qmflows.packages",
              "qmflows.parsers",
              "qmflows.templates"],
    package_data={
        "qmflows": ['data/dictionaries/*json']
    },
    classifiers=[
        'Intended Audience :: Science/Research',
        'Programming Language :: Python :: 3.7',
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Science/Research',
        'Topic :: Scientific/Engineering :: Chemistry'
    ],
    install_requires=['h5py', 'numpy', 'noodles==0.3.3', 'plams==1.4', 'pymonad',
                      'pyparsing', 'pyyaml==5.1', 'filelock'],
    extras_require={
        'test': ['pytest', 'pytest-cov', 'pytest-mock', 'nbsphinx', 'pygraphviz'],
        'doc': ['sphinx', 'sphinx_rtd_theme', 'nbsphinx']
    }
)
