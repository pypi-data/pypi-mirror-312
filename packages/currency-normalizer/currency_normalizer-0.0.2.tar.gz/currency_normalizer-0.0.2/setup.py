# this is setup.py

from setuptools import setup, find_packages
import setuptools
import subprocess
import os

setup(
    name='currency_normalizer',  # Package name
    version='0.0.2',  # Version of your package
    author='Enes Kuzucu',  # Your name

    description='A module to normalize currency strings',  # Short description
    long_description=open('README.md').read(),  # Long description from a README file
    long_description_content_type='text/markdown',  # Type of the long description

    packages=find_packages(),  # Automatically find packages in the directory
    install_requires=[ "pyyaml" ],
    include_package_data=True,
    package_data={
        'currency_normalizer': ['currencies.yaml'],
    },
    classifiers=[
        'Development Status :: 3 - Alpha',  # Development status
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',  # License as you choose
        'Programming Language :: Python :: 3',  # Supported Python versions
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.7',  # Minimum version requirement of Python
)