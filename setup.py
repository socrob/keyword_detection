#!/usr/bin/env python

from distutils.core import setup
from catkin_pkg.python_setup import generate_distutils_setup

# for your packages to be recognized by python
d = generate_distutils_setup(
 packages=['keyword_detection_ros'],
 package_dir={'keyword_detection_ros': 'src/keyword_detection_ros'}
)

setup(**d)
