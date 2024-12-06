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
"""Backward-compatibility imports for authentication interfaces
"""

from zope.authentication.interfaces import IAuthenticatedGroup
from zope.authentication.interfaces import IAuthentication
from zope.authentication.interfaces import IEveryoneGroup
from zope.authentication.interfaces import IFallbackUnauthenticatedPrincipal
from zope.authentication.interfaces import ILoginPassword
from zope.authentication.interfaces import ILogout
from zope.authentication.interfaces import ILogoutSupported
from zope.authentication.interfaces import IPrincipalSource
from zope.authentication.interfaces import IUnauthenticatedGroup
from zope.authentication.interfaces import IUnauthenticatedPrincipal
from zope.authentication.interfaces import PrincipalLookupError
# BBB
from zope.security.interfaces import IGroup
from zope.security.interfaces import IPermission
from zope.security.interfaces import IPrincipal
