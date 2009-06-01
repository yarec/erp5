# -*- coding: utf-8 -*-
##############################################################################
#
# Copyright (c) 2009 Nexedi SA and Contributors. All Rights Reserved.
#                    Łukasz Nowak <luke@nexedi.com>
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

from AccessControl import ClassSecurityInfo

from Products.ERP5Type import Permissions, PropertySheet, Constraint, interfaces

from Products.ERP5.Document.TradeModelLine import TradeModelLine
from Products.ERP5.Document.MappedValue import MappedValue

import zope.interface

class TradeModelCell(TradeModelLine, MappedValue):
    """Trade Model Line
    """
    meta_type = 'ERP5 Trade Model Cell'
    portal_type = 'Trade Model Cell'
    isCell = 1

    # Declarative security
    security = ClassSecurityInfo()
    security.declareObjectProtected(Permissions.AccessContentsInformation)

    # Declarative interfaces
    #    interfaces.IVariated as soon as interfaces.IVariated will be zope3
    zope.interface.implements(
        interfaces.ITransformation
    )

    # Declarative properties
    property_sheets = ( PropertySheet.Base
                    , PropertySheet.SimpleItem
                    , PropertySheet.Amount
                    , PropertySheet.Price
                    , PropertySheet.TradeModelLine
                    , PropertySheet.Predicate
                    , PropertySheet.MappedValue
                    , PropertySheet.ItemAggregation
                    )

    security.declareProtected( Permissions.AccessContentsInformation,
                               'hasCellContent' )
    def hasCellContent(self, base_id='movement'):
      """A cell cannot have cell content itself.
      """
      return 0

    def updateAggregatedAmountList(self, context, **kw):
      raise NotImplementedError('TODO')

    def getAggregatedAmountList(self, context, movement_list = None,
        current_aggregated_amount_list = None, **kw):
      raise NotImplementedError('TODO')

    security.declareProtected(Permissions.AccessContentsInformation,
                              'getPrice')
    def getPrice(self):
      return self._baseGetPrice()

    security.declareProtected(Permissions.AccessContentsInformation,
                              'getTotalPrice')
    def getTotalPrice(self):
      """
        Returns the totals price for this line
      """
      quantity = self.getQuantity() or 0.0
      price = self.getPrice() or 0.0
      return quantity * price
