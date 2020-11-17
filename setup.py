"""
from distutils.core import setup
from setuptools import find_packages
import os

current_directory = os.path.dirname(os.path.abspath(__file__))
try:
    with open(os.path.join(current_directory, 'README.md'), encoding='utf-8') as f:
        long_description = f.read()
except Exception:
    long_description = ''

setup(
    # Project name
    name='network-speedtest',
    # Packages to include in the distribution
    packages=find_packages(','),
    # Project version number
    version='1.0.0',
    # List a license for the project
    license='MIT',
    # Short description of your library
    description='Run a network speedtest at an interval - and write the results to a csv file',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='wnebyte',
    author_email='nan@gmail.com',
    url='https://github.com/wnebyte/network-speedtest-bg-task',
    keywords=[],
    install_requires=[
       'schedule',
        'speedtest'
    ]
)
"""