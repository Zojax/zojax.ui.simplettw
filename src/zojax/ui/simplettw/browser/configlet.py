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
from zope.component import getAdapters, queryMultiAdapter
from zope.traversing.browser import absoluteURL

from zojax.ui.simplettw.interfaces import ISimpleTTW, ITTWItemFactory


class SimpleTTWConfigletViewspace(object):

    def update(self):
        super(SimpleTTWConfigletViewspace, self).update()

        context = self.context
        request = self.request

        items = []
        for name, factory in getAdapters((context, request), ITTWItemFactory):
            items.append(
                (factory.title,
                 {'name': name,
                  'title': factory.title,
                  'description': factory.description,
                  'icon': queryMultiAdapter((factory,request), name='zmi_icon'),
                  'customized': factory.customItem is not None,
                  }))

        items.sort()
        self.items = [info for _t, info in items]

        self.isConfiglet = ISimpleTTW.providedBy(self.maincontext)
