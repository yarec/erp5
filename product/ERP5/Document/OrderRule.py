##############################################################################
#
# Copyright (c) 2002, 2005 Nexedi SARL and Contributors. All Rights Reserved.
#                    Jean-Paul Smets-Solanes <jp@nexedi.com>
#                    Romain Courteaud <romain@nexedi.com>
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
from Products.ERP5Type import Permissions, PropertySheet, Constraint, Interface
from Products.ERP5.Document.Rule import Rule
from Products.ERP5.Document.DeliveryRule import DeliveryRule
from zLOG import LOG

class OrderRule(DeliveryRule):
    """
      Order Rule object make sure an Order in the similation
      is consistent with the real order

      WARNING: what to do with movement split ?
    """

    # CMF Type Definition
    meta_type = 'ERP5 Order Rule'
    portal_type = 'Order Rule'

    # Declarative security
    security = ClassSecurityInfo()
    security.declareObjectProtected(Permissions.AccessContentsInformation)

    # Default Properties
    property_sheets = ( PropertySheet.Base
                      , PropertySheet.XMLObject
                      , PropertySheet.CategoryCore
                      , PropertySheet.DublinCore
                      )

    # Simulation workflow
    security.declareProtected(Permissions.ModifyPortalContent, 'expand')
    def expand(self, applied_rule, force=0, **kw):
      """
        Expands the current movement downward.
        -> new status -> expanded
        An applied rule can be expanded only if its parent movement
        is expanded.
      """
      delivery_line_type = 'Simulation Movement'
      # Get the order when we come from
      my_order = applied_rule.getDefaultCausalityValue()
      # Only expand if my_order is not None and state is not 'confirmed'
      if my_order is not None:
        # Only expand order rule if order not yet confirmed (This is consistent
        # with the fact that once simulation is launched, we stick to it)
        state = applied_rule.getLastExpandSimulationState()
        if force or \
           (state not in applied_rule.getPortalReservedInventoryStateList()\
           and state not in applied_rule.getPortalCurrentInventoryStateList()):
          # First, check each contained movement and make
          # a list of order ids which do not need to be copied
          # eventually delete movement which do not exist anylonger
          existing_uid_list = []
          existing_uid_list_append = existing_uid_list.append
          movement_type_list = applied_rule.getPortalMovementTypeList()
          order_movement_type_list = \
                                 applied_rule.getPortalOrderMovementTypeList()
          # Calculate existing simulation movement to delete
          for movement in applied_rule.contentValues(
                                filter={'portal_type': movement_type_list}):
            order_value = movement.getOrderValue(\
                                         portal_type=order_movement_type_list)
            if (order_value is None) or\
               (order_value.hasCellContent()):
              # XXX Make sure this is not deleted if already in delivery
              applied_rule._delObject(movement.getId())  
            else:
              existing_uid_list_append(order_value.getUid())
          # Build simulation movement if necessary
          for order_movement in my_order.getMovementList():
            try:
              if order_movement.getUid() not in existing_uid_list:
                # Generate a nicer ID
                if order_movement.getParentUid() ==\
                                      order_movement.getExplanationUid():
                  # We are on a line
                  new_id = order_movement.getId()
                else:
                  # On a cell
                  new_id = "%s_%s" % (order_movement.getParentId(),
                                      order_movement.getId())
                # Generate the simulation movement
                # Source, Destination, Quantity, Date, etc. are
                # acquired from the order and need not to be copied.
                new_sim_mvt = applied_rule.newContent(
                                portal_type=delivery_line_type,
                                id=new_id,
                                order_value=order_movement,
                                delivery_ratio=1,
                                deliverable=1,
                                **kw)
                                # No acquisition on variation_category_list 
                                # in this case to prevent user failure
            except AttributeError:
              LOG('ERP5: WARNING', 0,\
                  'AttributeError during expand on order movement %s'\
                  % order_movement.absolute_url())
          # Now we can set the last expand simulation state 
          # to the current state
          applied_rule.setLastExpandSimulationState(\
                                               my_order.getSimulationState())
      # Pass to base class
      Rule.expand(self, applied_rule, force=force, **kw)
