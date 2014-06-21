#!/usr/bin/env python

from distutils.core import setup

setup(name='LCARS',
      version='1.0.0.7',
      description='LCARS style GUI for Python. Requires pygame',
      author='James Fowkes',
      author_email='jamesfowkes@gmail.com',
      url='http://www.github.com/jamesfowkes/lcarsgui/',
	  packages=['LCARS', 'LCARS.Controls', 'LCARS.Sound'],
      package_dir={'LCARS':'.'},
	  package_data={'LCARS':['data/fonts/*', 'data/sfx/*']}
	  )
