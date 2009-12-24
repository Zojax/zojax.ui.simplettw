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
"""

$Id$
"""
from zope import interface, event
from zope.component import getUtility

from zojax.persistentpageelement.element import PageElement
from zojax.persistentpageelement.interfaces import IPageElementsConfiglet

from interfaces import ITTWPageElementFactory


class TTWPageElementFactory(object):
    interface.implements(ITTWPageElementFactory)

    name = None
    title = None
    description = None
    template = None

    def __init__(self, context, request):
        self.context = context
        self.request = request

    @property
    def source(self):
        return unicode(open(self.template).read(), 'utf8')

    @property
    def customItem(self):
        configlet = getUtility(IPageElementsConfiglet)

        if self.name in configlet:
            return configlet[self.name]

        return None

    def customize(self):
        configlet = getUtility(IPageElementsConfiglet)
        try:
            return configlet[self.name]
        except KeyError:
            element = PageElement(self.title, description=self.description)
            element.setSource(unicode(open(self.template).read(), 'utf8'))
            configlet[self.name] = element
            return configlet[self.name]
