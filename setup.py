#!/usr/bin/python

from distutils.core import setup

setup(name='langton',
      version='2.0',
      description="Enhanced Langton's ant cellular automata",
      author='Janne Blomqvist',
      author_email='Janne.Blomqvist@tkk.fi',
      url='http://users.tkk.fi/~jblomqvi/',
      scripts = ['langton.py', \
              'bufferedwindow.py']
     )

