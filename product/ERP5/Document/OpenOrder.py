##############################################################################
#
# Copyright (c) 2009 Nexedi SA and Contributors. All Rights Reserved.
#                    Jean-Paul Smets-Solanes <jp@nexedi.com>
#
# WARNING: This program as such is intended to be used by professional
# programmers who take the whole responsability of assessing all potential
# consequences resulting from its eventual inadequacies and bugs
# End users who are looking for a ready-to-use solution with commercial
# garantees and support are strongly adviced to contract a Free Software
# Service Company
#
# This program is Free Software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.
#
##############################################################################

from Globals import InitializeClass, PersistentMapping
from AccessControl import ClassSecurityInfo

from Products.ERP5Type import Permissions, PropertySheet, Constraint, interfaces
from Products.ERP5.Document.Delivery import Delivery

class OpenOrder(Delivery):
  """
    An OpenOrder is a collection of Open Order Lines
  """
  meta_type = 'ERP5 Open Order'
  portal_type = 'Open Order'
  isPredicate = 1 # XXX - Why ?

  # Declarative security
  security = ClassSecurityInfo()
  security.declareObjectProtected(Permissions.AccessContentsInformation)

  # Declarative interfaces
  __implements__ = (interfaces.IExpandable, interfaces.IOpenOrderExpander)

  # Declarative properties
  property_sheets = ( PropertySheet.Base
                    , PropertySheet.XMLObject
                    , PropertySheet.CategoryCore
                    , PropertySheet.DublinCore
                    , PropertySheet.Folder
                    , PropertySheet.Comment
                    , PropertySheet.Arrow
                    , PropertySheet.Order
                    )

  # Expandable Interface Implementation
  def expand(self, *args, **kw):
    """
      Any Open Order Line / Open Order Cell which does not relate
      (aggregate) to a Subscription Item must be expanded
      through the default rule. 

      What would be nice is to use the SubscriptionItemRule to expand
      lines one by one so that an Item can be used at any time.
      expansion logic is provided by the OpenOrder or by the 
      SubscriptionItem

      Others are expanded by their Item
    """
    
  security.declarePrivate('expandOpenOrderRule')
  def expandOpenOrderRule(self, applied_rule_id=None, force=0, **kw):
    """
      Provides the default implementation of expand for Open Orders
    """

