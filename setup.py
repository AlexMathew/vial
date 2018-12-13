#!/usr/bin/env python3
# -*- coding: utf-8 -*-

try:
    from setuptools import setup, find_packages
except ImportError:
    from distutils.core import setup, find_packages


readme = open('README.md').read()
requirements = open('requirements.txt').read().split('\n')
test_requirements = open('test_requirements.txt').read().split('\n')

setup(
    name='vial',
    version='0.1.0',
    description='A web framework on just http.server (without using pre-existing ORMs)',
    long_description=readme,
    author='Alex Mathew',
    author_email='alexmathew003@gmail.com',
    url='https://alexmathew.github.io/vial',
    packages=find_packages(exclude=('tests',)),
    package_dir={'vial':
                 'vial'},
    include_package_data=True,
    install_requires=requirements,
    license="MIT",
    keywords=[],
    entry_points={
        'console_scripts': ['vial=vial.run:cli']
    },
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.7',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    test_suite='tests',
    tests_require=test_requirements
)

print("\nVial has been installed. Use ```vial --help``` for instructions\n")
