##############################################################################
#
# Copyright (c) 2009 Zope Foundation and Contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
##############################################################################
""" Setup for zojax.ui.simplettw package

$Id$
"""
import sys, os
from setuptools import setup, find_packages

def read(*rnames):
    return open(os.path.join(os.path.dirname(__file__), *rnames)).read()

version='0'


setup(name = 'zojax.ui.simplettw',
      version = version,
      author = 'Anatoly Bubenkov, Nikolay Kim',
      author_email = 'bubenkoff@gmail.com',
      description = "Simple ttw customization for zojax themes",
      long_description = (
          'Detailed Documentation\n' +
          '======================\n'
          + '\n\n' +
          read('CHANGES.txt')
          ),
      classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Zope Public License',
        'Programming Language :: Python',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Topic :: Internet :: WWW/HTTP',
        'Framework :: Zope3'],
      url='http://zojax.net/',
      license='ZPL 2.1',
      packages=find_packages('src'),
      package_dir = {'':'src'},
      namespace_packages=['zojax','zojax.ui'],
      install_requires = ['setuptools',
                          'zope.component',
                          'zope.interface',
                          'zope.dublincore',
                          'zope.traversing',
                          'zope.lifecycleevent',
                          'zope.location',
                          'zope.event',
                          'zope.security',
                          'zope.publisher',
                          'zope.configuration',
                          'zope.i18n',
                          'zope.i18nmessageid',

                          'z3c.traverser',

                          'zojax.filefield',
                          'zojax.pageelement',
                          'zojax.resource',
                          'zojax.controlpanel',
                          'zojax.persistentresource',
                          'zojax.persistentpageelement',
                          'zojax.statusmessage',
                          ],
      extras_require = dict(test=['zope.app.testing',
                                  'zope.testing',
                                  'zope.testbrowser',
                                  'zope.app.folder',
                                  'zope.app.zcmlfiles',
                                  'zope.securitypolicy',
                                  'zojax.layout',
                                  'zojax.statusmessage',
                                  'zojax.autoinclude',
                                  ]),
      include_package_data = True,
      zip_safe = False
      )
