#!/usr/bin/env python
#-*- encoding: utf-8 -*-

from distutils.core import setup

setup(name='pantheradesktop',
      description = "Panthera Desktop Framework",
      long_description = "Tiny desktop framework for easy application development in Python using PyQT/PySide",
      author = "Damian Kęska",
      author_email = "webnull.www@gmail.com",
      version="0.1.0.2",
      license = "LGPL",
      package_dir={'': 'src'},      
      packages=['pantheradesktop'],
      data_files = []
     )
