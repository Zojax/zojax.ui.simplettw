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
import os.path
from zope import interface, schema
from zope.component.zcml import adapter
from zope.traversing.namespace import queryResource
from zope.security.checker import defineChecker, Checker, CheckerPublic
from zope.configuration.fields import Path, Tokens, MessageID
from zope.configuration.fields import GlobalObject, GlobalInterface
from zope.configuration.exceptions import ConfigurationError
from zope.publisher.interfaces.browser import IDefaultBrowserLayer
from zope.app.component.hooks import getSite

from zojax.resource.zcml import resourceDirective
from zojax.pageelement.zcml import pageelementDirective
from zojax.persistentresource.interfaces import IStaticResource

from resource import TTWResourceFactory
from element import TTWPageElementFactory
from interfaces import \
    ITTWItemFactory, ITTWPageElementFactory, ITTWResourceFactory, ISimpleTTW


class ITTWElementDirective(interface.Interface):
    """A directive to register a new ttw element. """

    name = schema.TextLine(
        title = u"The name of the ttw element.",
        description = u"The name shows up in URLs/paths. For example 'foo'.",
        required = True)

    title = MessageID(
        title = u'Title',
        required = True)

    description = MessageID(
        title = u'Description',
        required = False)

    template = Path(
        title = u'Page element template.',
        description = u"Refers to a file containing a page template (should " \
            "end in extension ``.pt`` or ``.html``).",
        required=True)

    layer = GlobalObject(
        title = u'Layer',
        description = u'The layer for which the element should be available',
        required = False,
        default = IDefaultBrowserLayer)


def ttwElementDirective(
    _context, name, title, for_ = interface.Interface,
    description=u'', layer = IDefaultBrowserLayer, template=u''):

    # register pageelement
    pageelementDirective(
        _context, name, for_=for_,
        title=title, description=description, layer=layer, template=template)

    # Make sure that the template exists
    template = os.path.abspath(str(_context.path(template)))
    if not os.path.isfile(template):
        raise ConfigurationError("No such file", template)

    # Build a new class that we can use different permission settings if we
    # use the class more then once.
    cdict = {}
    cdict['name'] = name
    cdict['title'] = title
    cdict['description'] = description
    cdict['template'] = template

    newclass = type(
        str('<TTWResourceFactory %s>'%name), (TTWPageElementFactory,), cdict)

    # Set up permission mapping for various accessible attributes
    required = {}
    for iname in ITTWPageElementFactory:
        required[iname] = CheckerPublic

    # security checker
    defineChecker(newclass, Checker(required))

    # register the page element
    adapter(_context, (newclass,), ITTWItemFactory, (for_, layer), name=name)


class ITTWResourceDirective(interface.Interface):
    """A directive to register a new ttw element. """

    name = schema.TextLine(
        title = u"The name of the resource.",
        description = u"The name shows up in URLs/paths. For example 'foo'.",
        required = True)

    type = schema.ASCIILine(
        title = u"Content type of the resource.",
        description = u"Mime type. For example 'text/plain'.",
        default = '',
        required = False)

    title = MessageID(
        title = u'Title',
        required = True)

    description = MessageID(
        title = u'Description',
        required = False)

    file = Path(
        title = u'Default resource file.',
        description = u"Refers to a file containing a default resource",
        required=True)

    layer = GlobalObject(
        title = u'Layer',
        description = u'The layer for which the element should be available',
        required = False,
        default = IDefaultBrowserLayer)


def ttwResourceDirective(
    _context, name, title, for_ = interface.Interface,
    layer = IDefaultBrowserLayer, type = '', file = None, description=u'', **kwargs):

    rname = u'simplettw.%s'%name
    # register resource
    resourceDirective(
        _context, rname, file, layer, permission='zope.Public', type='')

    # Build a new class that we can use different permission settings if we
    # use the class more then once.
    cdict = {}
    cdict['name'] = name
    cdict['title'] = title
    cdict['description'] = description
    cdict['file'] = os.path.abspath(str(_context.path(file)))
    cdict['contentType'] = type

    newclass = Type(
        str('<TTWResourceFactory %s>'%name), (TTWResourceFactory,), cdict)

    # Set up permission mapping for various accessible attributes
    required = dict([(iname, CheckerPublic) for iname in ITTWResourceFactory])
    defineChecker(newclass, Checker(required))

    # register the resource element
    adapter(_context, (newclass,), ITTWItemFactory, (ISimpleTTW, layer), name=name)

    # register IStaticResource adapter
    adapter(_context, (StaticResource(rname),),
            IStaticResource, (layer,), name=name)


Type = type


class StaticResource(object):
    interface.implements(IStaticResource)

    def __init__(self, name):
        self.name = name

    def __call__(self, request):
        return queryResource(getSite(), self.name, request)
