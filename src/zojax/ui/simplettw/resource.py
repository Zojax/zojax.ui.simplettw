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
from zope.component import queryMultiAdapter, getAdapters, getUtility
from zope.lifecycleevent import ObjectModifiedEvent

from zojax.filefield.data import FileData
from zojax.persistentresource.file import FileResource
from zojax.persistentresource.interfaces import IPersistentResources

from interfaces import ITTWResourceFactory


class TTWResourceFactory(object):
    interface.implements(ITTWResourceFactory)

    name = None
    title = None
    description = None
    file = None
    mimeType = None

    def __init__(self, context, request):
        self.context = context
        self.request = request

    @property
    def customItem(self):
        configlet = getUtility(IPersistentResources)
        try:
            res = configlet[self.name]
            if self.contentType and res.data.mimeType != self.contentType:
                res.data.mimeType = self.contentType
            return res
        except KeyError:
            pass

        return None

    def customize(self):
        configlet = getUtility(IPersistentResources)
        name = self.name
        try:
            return configlet[name]
        except KeyError:
            element = FileResource(self.title, description=self.description)
            if self.file:
                element.data = FileData(open(self.file), mimeType=self.mimeType)
            configlet[name] = element
            event.notify(ObjectModifiedEvent(element))
            return element
