##############################################################################
#
# Copyright (c) 2002 Nexedi SARL and Contributors. All Rights Reserved.
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

from AccessControl import ClassSecurityInfo

from Products.ERP5Type import Permissions, PropertySheet, Constraint, Interface
from Products.ERP5Type.Base import Base

from Products.ERP5.Document.Coordinate import Coordinate

import re

class Telephone(Coordinate, Base):
    """
        A telephone is a coordinate which stores a telephone number
        The telephone class may be used by multiple content types (ex. Fax,
        Mobile Phone, Fax, Remote Access, etc.).

        A telephone is a terminating leaf
        in the OFS. It can not contain anything.

        Telephone inherits from Base and
        from the mix-in Coordinate

        A list of I18N telephone codes can be found here::
          http://kropla.com/dialcode.htm
    """

    meta_type = 'ERP5 Telephone'
    portal_type = 'Telephone'
    add_permission = Permissions.AddPortalContent
    isPortalContent = 1
    isRADContent = 1

    # Declarative security
    security = ClassSecurityInfo()
    security.declareObjectProtected(Permissions.AccessContentsInformation)

    # Declarative properties
    property_sheets = ( PropertySheet.Base
                      , PropertySheet.SimpleItem
                      , PropertySheet.Telephone
                      )


    security.declareProtected(Permissions.ModifyPortalContent, 'fromText')
    def fromText(self, coordinate_text):
      """ See ICoordinate.fromText """
      method = self._getTypeBasedMethod('fromText')
      if method is not None:
        return method(text=coordinate_text)
      
      if coordinate_text is None:
        coordinate_text = ''

      #This regexp get the coordinate text and extract only numbers
      onlynumber = ''.join(re.findall('[0-9]', coordinate_text))
      ScriptgetRegexp = getattr(self, 'Telephone_getRegexp', None)
      
      #Test if coordinate_text has or not markups.
      if len(coordinate_text) > len(onlynumber):
        #trying to get a possible contry number to be used by script
        country=re.match('((\+|)(?P<country>\d*))',coordinate_text).groupdict().get('country','')
        if ScriptgetRegexp is not None:
            temp_object = ScriptgetRegexp(index=country)
            input_parser = temp_object.input
            number_match = re.match(input_parser, coordinate_text)
            if not number_match:
              return
            number_dict = number_match.groupdict()
      else:
        number_dict={'number':coordinate_text}
      
      country=number_dict.get('country','')
      area=number_dict.get('area','')
      number=number_dict.get('number','')
      ext=number_dict.get('ext','')

      if ((country in ['', None]) and \
          (area in ['', None]) and \
          (number in ['', None]) and \
          (ext in ['', None])):
        country=area=number=extension=''
      else:
        #The country and area is trying to get from dict, 
        #but if it fails must be get from preference
        country = (number_dict.get('country') or \
                   self.portal_preferences.default_site_preference.getPreferredTelephoneDefaultCountryNumber() or \
                   '').strip()
        area = (number_dict.get('area') or \
                self.portal_preferences.default_site_preference.getPreferredTelephoneDefaultAreaNumber() or 
                '').strip()
        number = (number_dict.get('number') or '').strip().replace('-', '').replace(' ','')
        extension = (number_dict.get('ext') or '').strip()

      self.edit(telephone_country = country,
                telephone_area = area,
                telephone_number = number, 
                telephone_extension = extension)
     
    security.declareProtected(Permissions.ModifyPortalContent, '_setText')
    _setText = fromText

    security.declareProtected(Permissions.View, 'asText')
    def asText(self):
      """
        Returns the telephone number in standard format
      """
      script = self._getTypeBasedMethod('asText')
      if script is not None:
        return script()
      
      telephone_country = self.getTelephoneCountry() or ''
      telephone_area = self.getTelephoneArea() or ''
      telephone_number = self.getTelephoneNumber() or ''
      telephone_extension = self.getTelephoneExtension() or ''
     
      # If country, area, number, extension are blank the method
      # should to return blank.
      if ((telephone_country == '') and \
          (telephone_area == '') and \
          (telephone_number == '') and \
          (telephone_extension == '')): 
        return ''
      
      # Trying to get the notation from Telephone_getRegexp script 
      ScriptgetRegexp = getattr(self, 'Telephone_getRegexp', None)
      if ScriptgetRegexp is not None:
        temp_object = ScriptgetRegexp(index=telephone_country)
        notation = temp_object.notation
      else:
        notation = ''

      if notation not in [None, '']:
        notation=notation.replace('<country>',telephone_country)
        notation=notation.replace('<area>',telephone_area)
        notation=notation.replace('<number>',telephone_number)
        notation=notation.replace('<ext>',telephone_extension)

      return notation

    security.declareProtected(Permissions.AccessContentsInformation,
                              'asURL')
    def asURL(self):
      """Returns a text representation of the Url if defined
      or None else.
      """
      telephone_country = self.getTelephoneCountry()
      if telephone_country is not None:
        url_string = '+%s' % telephone_country
      else :
        url_string = '0'

      telephone_area = self.getTelephoneArea()
      if telephone_area is not None:
        url_string += telephone_area

      telephone_number = self.getTelephoneNumber()
      if telephone_number is not None:
        url_string += telephone_number

      if url_string == '0':
        return None
      return 'tel:%s' % (url_string.replace(' ',''))

    security.declareProtected(Permissions.View, 'getText')
    getText = asText

    security.declareProtected(Permissions.View, 'standardTextFormat')
    def standardTextFormat(self):
        """
          Returns the standard text formats for telephone numbers
        """
        return ("+33(0)6-62 05 76 14",)

