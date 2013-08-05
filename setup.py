#!python3.3
# -*- coding: utf-8 -*-
#from distutils.core import setup

from ez_setup import use_setuptools
use_setuptools()
from setuptools import setup

import sys
import os

DISTUTILS_DEBUG = True

py_version = sys.version_info[:2]
PY3 = py_version[0] == 3

if not PY3:
    raise RuntimeError('Python 3.x is required')

thisdir = os.path.dirname(__file__)

with open(os.path.join(thisdir, 'README')) as file:
    long_description = file.read()

setup(name = 'pyWavefront3D',
      version = '0.0.0',  # major.minor.revision
      
      platforms = ['Linux', 'Windows'],
      url = 'https://github.com/Rod-Persky/pyWavefront3D',
      
      classifiers = [
        'Development Status :: 3 - Alpha',
        
        'Topic :: Scientific/Engineering',
        'Topic :: Scientific/Engineering :: Electronic Design Automation (EDA)',
        'Topic :: Scientific/Engineering :: Physics',
        'Topic :: Scientific/Engineering :: Visualization',
        
        'License :: OSI Approved :: Academic Free License (AFL)',
        
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.2",
        "Programming Language :: Python :: 3.3",
        
        'Intended Audience :: End Users/Desktop',
        'Intended Audience :: Developers',
        'Intended Audience :: Manufacturing',
        'Intended Audience :: Science/Research',
        
        'Environment :: Console',
        'Environment :: No Input/Output (Daemon)',  # No IO required
        
        'Natural Language :: English',
        
        'Operating System :: MacOS',
        'Operating System :: Microsoft',
        'Operating System :: POSIX',
        'Operating System :: OS Independent',
        ],

      description = 'Python Alias Wavefront .OBJ geometry export system',
      long_description = long_description,
      license = 'Academic Free License ("AFL") v. 3.0',

      author = 'Rodney Persky',
      author_email = 'rodney.persky@gmail.com',

      packages = ['pyWavefront3D'],
      package_dir = {'pyWavefront3D': 'pyWavefront3D'},
      
      zip_safe = True,
      include_package_data = True
      )
