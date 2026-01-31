#!/usr/bin/python

from distutils.core import setup

setup(name='langton',
      version='3.99',
      description="Enhanced Langton's ant cellular automata",
      author='Janne Blomqvist',
      author_email='blomqvist.janne@gmail.com',
      url='',
      scripts = ['langton.py', \
              'qtlangton.py']
     )

