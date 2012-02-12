#!/usr/bin/env python
"""
    Jean-Lou Dupont's Simple Toolkit
    
    Created on 2012-01-19
    @author: jldupont
"""
__author__  ="Jean-Lou Dupont"
__version__ ="0.1.0"


from distutils.core import setup
from setuptools import find_packages


setup(name=         'sipi',
      version=      __version__,
      description=  'Collection of tools',
      author=       __author__,
      author_email= 'jl@jldupont.com',
      url=          'http://jldupont.github.com/sipi/doc/_build/',
      package_dir=  {'': "src",},
      packages=     find_packages("src"),
      scripts=      [
                     ],                     
      zip_safe=False
      ,install_requires=["pyfnc >= 0.1.0"]
      )
