##############################################################################
#
# Copyright (c) 2001, 2002 Zope Foundation and Contributors.
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
"""Backward-compatibility imports for the global principal registry

"""

# BBB: these were moved to zope.principalregistry
from zope.principalregistry.principalregistry import AuthenticatedGroup
from zope.principalregistry.principalregistry import DuplicateId
from zope.principalregistry.principalregistry import DuplicateLogin
from zope.principalregistry.principalregistry import EverybodyGroup
from zope.principalregistry.principalregistry import Group
from zope.principalregistry.principalregistry import Principal
from zope.principalregistry.principalregistry import PrincipalBase
from zope.principalregistry.principalregistry import PrincipalRegistry
from zope.principalregistry.principalregistry import UnauthenticatedGroup
from zope.principalregistry.principalregistry import UnauthenticatedPrincipal
from zope.principalregistry.principalregistry import \
    fallback_unauthenticated_principal
from zope.principalregistry.principalregistry import principalRegistry
