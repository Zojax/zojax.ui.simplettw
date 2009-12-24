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
""" simple ttw configlet interfaces

$Id$
"""
from zope import schema, interface
from zope.i18nmessageid import MessageFactory

_ = MessageFactory('zojax.ui.simplettw')


class ISimpleTTW(interface.Interface):
    """ configlet interface """


class ITTWItemFactory(interface.Interface):
    """ ttw item factory"""

    name = interface.Attribute('name')

    title = schema.TextLine(
        title = u'Title',
        description = u'Element title.',
        required = True)

    description = schema.TextLine(
        title = u'Description',
        description = u'Short description of element.',
        required = False)

    customItem = interface.Attribute('Custom item')

    def customize():
        """ create custom item """


class ITTWPageElementFactory(ITTWItemFactory):
    """ ttw page element factory"""

    source = interface.Attribute('Template source')

    template = interface.Attribute('Template')


class ITTWResourceFactory(ITTWItemFactory):
    """ ttw resource factory"""

    file = interface.Attribute('File')
