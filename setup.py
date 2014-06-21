#!/usr/bin/env python

from distutils.core import setup

setup(name='LCARS',
      version='1.1.0.0',
      description='LCARS style GUI',
      author='Grey Knight<tinyplasticgreyknight@yahoo.com>, James Fowkes<jamesfowkes@gmail.com>',
      author_email='tinyplasticgreyknight@yahoo.com',
      url='http://www.github.com/tinyplasticgreyknight/LCARS/',
	  packages=['LCARS', 'LCARS.Controls', 'LCARS.Sound'],
      package_dir={'LCARS':'.'},
	  package_data={'LCARS':['data/fonts/*', 'data/sfx/*']}
	  )
