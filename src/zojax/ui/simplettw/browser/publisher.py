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
from zope import interface, component
from zope.location import LocationProxy
from zope.component import getUtility, queryMultiAdapter
from zope.publisher.interfaces import NotFound
from zope.publisher.interfaces.browser import IBrowserPublisher
from z3c.traverser.interfaces import ITraverserPlugin

from zojax.ui.simplettw.interfaces import ISimpleTTW, ITTWItemFactory


class ConfigletPublisher(object):
    interface.implements(ITraverserPlugin)
    component.adapts(ISimpleTTW, interface.Interface)

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def publishTraverse(self, request, name):
        context = self.context

        factory = queryMultiAdapter((context, request), ITTWItemFactory, name)
        if factory is not None:
            item = factory.customItem
            if item is not None:
                return LocationProxy(item, context, name)
            return LocationProxy(factory, context, name)

        view = queryMultiAdapter((context, request), name=name)
        if view is not None:
            return view

        raise NotFound(context, name, request)

    def browserDefault(self, request):
        return self, ('index.html',)
