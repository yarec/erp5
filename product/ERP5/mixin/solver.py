# -*- coding: utf-8 -*-
##############################################################################
#
# Copyright (c) 2009 Nexedi SA and Contributors. All Rights Reserved.
#                    Jean-Paul Smets-Solanes <jp@nexedi.com>
#
# WARNING: This program as such is intended to be used by professional
# programmers who take the whole responsibility of assessing all potential
# consequences resulting from its eventual inadequacies and bugs
# End users who are looking for a ready-to-use solution with commercial
# guarantees and support are strongly adviced to contract a Free Software
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
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
##############################################################################

import zope.interface
from AccessControl import ClassSecurityInfo
from Products.ERP5Type import Permissions, PropertySheet, interfaces
from Products.ERP5Type.XMLObject import XMLObject
from Products.ERP5.mixin.configurable import ConfigurableMixin

class SolverMixin(object):
  """
  Provides generic methods and helper methods to implement ISolver.
  """
  # Declarative security
  security = ClassSecurityInfo()
  security.declareObjectProtected(Permissions.AccessContentsInformation)

  # Declarative interfaces
  zope.interface.implements(interfaces.ISolver,)

  # Implementation of ISolver

  def getPortalTypeValue(self):
    return self.getPortalObject().portal_solvers._getOb(self.getPortalType())

  def searchDeliverySolverList(self, **kw):
    """
    this method returns a list of delivery solvers

    XXX here we cannot test delivery solver as a predicate, because
    predicate's context should be Solver Decision, not a target
    solver.
    """
    target_solver_type = self.getPortalTypeValue()
    solver_list = target_solver_type.getDeliverySolverValueList()
    return solver_list

class ConfigurablePropertySolverMixin(SolverMixin,
                                      ConfigurableMixin,
                                      XMLObject):
  """
  Base class for Target Solvers that can be applied to many
  solver-decisions of a solver process, and need to accumulate the
  tested_property_list configuration among all solver-decisions
  """

  add_permission = Permissions.AddPortalContent
  isIndexable = 0 # We do not want to fill the catalog with objects on which we need no reporting

  # Declarative security
  security = ClassSecurityInfo()
  security.declareObjectProtected(Permissions.AccessContentsInformation)

  zope.interface.implements(interfaces.ISolver,
                            interfaces.IConfigurable,)

  # Default Properties
  property_sheets = ( PropertySheet.Base
                    , PropertySheet.XMLObject
                    , PropertySheet.CategoryCore
                    , PropertySheet.DublinCore
                    , PropertySheet.TargetSolver
                    )

  def getTestedPropertyList(self):
    configuration_dict = self.getConfigurationPropertyDict()
    tested_property_list = configuration_dict.get('tested_property_list')
    if tested_property_list is None:
      portal_type = self.getPortalObject().portal_types.getTypeInfo(self)
      tested_property_list = portal_type.getTestedPropertyList()
    return tested_property_list
