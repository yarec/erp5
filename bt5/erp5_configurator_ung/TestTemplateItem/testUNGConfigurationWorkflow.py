##############################################################################
# Copyright (c) 2011 Nexedi SA and Contributors. All Rights Reserved.
#                     Gabriel M. Monnerat <gabriel@tiolive.com>
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

from Products.ERP5Type.tests.ERP5TypeTestCase import ERP5TypeTestCase
from Products.ERP5Type.tests.Sequence import SequenceList

class TestUNGConfiguratorWorkflow(ERP5TypeTestCase):
  """
    Test Live UNG Configuration Workflow.
  """

  standard_bt5_list = ('erp5_ingestion_mysql_innodb_catalog',
                       'erp5_simulation',
                       'erp5_dhtml_style',
                       'erp5_jquery',
                       'erp5_jquery_ui',
                       'erp5_web',
                       'erp5_ingestion',
                       'erp5_dms',
                       'erp5_crm',
                       'erp5_knowledge_pad',
                       'erp5_jquery_plugin_spinbtn',
                       'erp5_jquery_plugin_jgraduate',
                       'erp5_jquery_plugin_svgicon',
                       'erp5_jquery_plugin_hotkey',
                       'erp5_jquery_plugin_jquerybbq',
                       'erp5_jquery_plugin_svg_editor',
                       'erp5_jquery_plugin_sheet',
                       'erp5_jquery_plugin_mbmenu',
                       'erp5_jquery_plugin_jqchart',
                       'erp5_jquery_plugin_colorpicker',
                       'erp5_jquery_plugin_elastic',
                       'erp5_jquery_plugin_wdcalendar',
                       'erp5_jquery_sheet_editor',
                       'erp5_xinha_editor',
                       'erp5_svg_editor',
#                      'erp5_mail_reader',
                       'erp5_web_ung_core',
                       'erp5_web_ung_theme',
                       'erp5_web_ung_role')

  DEFAULT_SEQUENCE_LIST = """
     stepCreateBusinessConfiguration
     stepSetUNGWorkflow
     stepConfiguratorNext
     stepTic
     stepCheckBT5ConfiguratorItem
     stepCheckConfigureOrganisationForm
     stepSetupOrganisationConfiguratorItem
     stepConfiguratorNext
     stepTic
     stepCheckConfigureUserAccountNumberForm
     stepCheckOrganisationConfiguratorItem
     stepSetupUserAccountNumberThree
     stepConfiguratorNext
     stepTic
     stepCheckConfigureMultipleUserAccountForm
     stepSetupMultipleUserAccountThree
     stepConfiguratorNext
     stepTic
     stepCheckConfigurePreferenceForm
     stepSetupPreferenceConfigurationBrazil
     stepConfiguratorNext
     stepTic
     stepCheckConfigureWebSiteForm
     stepSetupWebSiteConfiguration
     stepConfiguratorNext
     stepTic
     stepCheckConfigureInstallationForm
     stepSetupInstallConfiguration
     stepConfiguratorNext
     stepTic
     stepCheckInstallConfiguration
     stepStartConfigurationInstallation
     stepTic
     stepCheckUNGWebSiteAfterInstallation
  """

  def getBusinessTemplateList(self):
    return ('erp5_core_proxy_field_legacy',
            'erp5_full_text_myisam_catalog',
            'erp5_base',
            'erp5_workflow',
            'erp5_configurator',
            'erp5_configurator_ung',)

  def afterSetUp(self):
    self.portal.portal_templates.updateRepositoryBusinessTemplateList(
                           ['http://www.erp5.org/dists/snapshot/bt5/'])

  def stepCreateBusinessConfiguration(self,  sequence=None, sequence_list=None, **kw):
    """ Create one Business Configuration """
    module = self.portal.business_configuration_module
    business_configuration = module.newContent(
                               portal_type="Business Configuration",
                               title='Test Configurator UNG Workflow')
    next_dict = {}
    sequence.edit(business_configuration=business_configuration, 
                  next_dict=next_dict)

  def stepSetUNGWorkflow(self, sequence=None, sequence_list=None, **kw):
    """ Set UNG Workflow into Business Configuration """
    business_configuration = sequence.get("business_configuration")
    self.setBusinessConfigurationWorkflow(business_configuration,
                                   "workflow_module/ung_configuration_workflow")

  def assertCurrentStep(self, step_title, server_response):
    """ Checks the current step title. """
    self.assertTrue(
      '<h2>%s</h2>' % step_title in server_response['data'],
      'Unable to guess current step title (expected:%s) in: \n%s' %
      (step_title, server_response))

  def stepConfiguratorNext(self, sequence=None, sequence_list=None, **kw):
    """ Go Next into Configuration """
    business_configuration = sequence.get("business_configuration")
    next_dict = sequence.get("next_dict")
    response_dict = self.portal.portal_configurator._next(
                            business_configuration, next_dict)

    sequence.edit(response_dict=response_dict)

  def setBusinessConfigurationWorkflow(self, business_configuration, workflow):
    """ Set configurator workflow """
    business_configuration.setResource(workflow)

  def stepCheckBT5ConfiguratorItem(self, sequence=None, sequence_list=None, **kw):
    """ Check if the Configuration Item list is correct """
    business_configuration = sequence.get("business_configuration")
    # second one: install some standard business templates
    standard_bt5_config_save = business_configuration['1']
    self.assertEquals(len(self.standard_bt5_list),
          len(standard_bt5_config_save.contentValues(
                  portal_type='Standard BT5 Configurator Item')))
    self.assertEquals(
      set(self.standard_bt5_list),
      set([x.bt5_id for x in standard_bt5_config_save.contentValues()]))

  def stepCheckConfigureOrganisationForm(self, sequence=None, sequence_list=None, **kw):
    """ Check if Confire Configure step was showed """
    response_dict = sequence.get("response_dict")
    if 'command' in response_dict:
      self.assertEquals('show', response_dict['command'])
    self.assertEquals(None, response_dict['previous'])
    self.assertEquals('Configure Organisation', response_dict['next'])
    self.assertCurrentStep('Your Organisation', response_dict)

  def stepSetupOrganisationConfiguratorItem(self, sequence=None, sequence_list=None, **kw):
    """ Create one Organisation with Basic information """
    next_dict = dict(
        field_your_title='My Organisation',
        field_your_default_email_text='me@example.com',
        field_your_default_telephone_text='01234567890',
        field_your_default_address_street_address='.',
        field_your_default_address_zip_code='59000')
    sequence.edit(next_dict=next_dict)

  def stepCheckConfigureUserAccountNumberForm(self, sequence=None, sequence_list=None, **kw):
    """ """
    response_dict = sequence.get("response_dict")
    if 'command' in response_dict:
      self.assertEquals('show', response_dict['command'])
    self.assertEquals('Configure user accounts number', response_dict['next'])
    self.assertEquals('Previous', response_dict['previous'])
    self.assertCurrentStep('Number of user accounts', response_dict)

  def stepCheckOrganisationConfiguratorItem(self, sequence=None, sequence_list=None, **kw):
    """ Check if organisation was created fine """
    business_configuration = sequence.get("business_configuration")
    organisation_config_save = business_configuration['3']
    self.assertEquals(organisation_config_save.getTitle(),
                      "My Organisation")
    self.assertEquals(1, len(organisation_config_save.contentValues()))
    organisation_config_item = organisation_config_save['1']
    self.assertEquals(organisation_config_item.getPortalType(),
                      'Organisation Configurator Item')
    self.assertEquals(organisation_config_item.getDefaultEmailText(),
                      'me@example.com')

  def stepSetupUserAccountNumberThree(self, sequence=None, sequence_list=None, **kw):
    """ Create one more user account """
    next_dict = dict(field_your_user_number="3")
    sequence.edit(next_dict=next_dict)

  def stepCheckConfigureMultipleUserAccountForm(self, sequence=None, sequence_list=None, **kw):
    """ Check the multiple user account form """
    response_dict = sequence.get("response_dict")
    if 'command' in response_dict:
      self.assertEquals('show', response_dict['command'])
    self.assertEquals('Previous', response_dict['previous'])
    self.assertEquals('Configure user accounts', response_dict['next'])
    self.assertCurrentStep('Configuration of users', response_dict)
 
  def stepSetupMultipleUserAccountThree(self, sequence=None, sequence_list=None, **kw):
    """ Create multiple user account """
    user_list = [
      dict(
        field_your_first_name='Person',
        field_your_last_name='Creator',
        field_your_reference="person_creator",
        field_your_password='person_creator',
        field_your_password_confirm='person_creator',
        field_your_default_email_text='test@test.com',
        field_your_default_telephone_text='',
      ), dict(
        field_your_first_name='Person',
        field_your_last_name='Assignee',
        field_your_reference="person_assignee",
        field_your_password='person_assignee',
        field_your_password_confirm='person_assignee',
        field_your_default_email_text='test@test.com',
        field_your_default_telephone_text='',
      ), dict(
        field_your_first_name='Person',
        field_your_last_name='Assignor',
        field_your_reference="person_assignor",
        field_your_password='person_assignor',
        field_your_password_confirm='person_assignor',
        field_your_default_email_text='test@test.com',
        field_your_default_telephone_text='',
      ),
    ]
    next_dict = {}
    for user in user_list:
      for k, v in user.items():
        next_dict.setdefault(k, []).append(v)
    sequence.edit(next_dict=next_dict)

  def stepCheckConfigurePreferenceForm(self, sequence=None, sequence_list=None, **kw):
    """ Check the multiple user account form """
    response_dict = sequence.get("response_dict")
    if 'command' in response_dict:
      self.assertEquals('show', response_dict['command'])
    self.assertEquals('Previous', response_dict['previous'])
    self.assertEquals('Configure user accounts', response_dict['next'])
    self.assertCurrentStep('Configuration of users', response_dict)

  def stepCheckConfigurePreferenceForm(self, sequence=None, sequence_list=None, **kw):
    """ Check the multiple user account form """
    response_dict = sequence.get("response_dict")
    if 'command' in response_dict:
      self.assertEquals('show', response_dict['command'])
    self.assertEquals('Previous', response_dict['previous'])
    self.assertEquals('Configure ERP5 Preferences', response_dict['next'])
    self.assertCurrentStep('ERP5 preferences', response_dict)

  def stepSetupPreferenceConfigurationBrazil(self, sequence=None, sequence_list=None, **kw):
    """ Setup the Brazil preference configuration """
    next_dict = dict(field_your_preferred_date_order='dmy',
                     field_your_lang='erp5_l10n_pt-BR',
                     field_your_preferred_event_sender_email="test@test.com",
                     default_field_your_lang=1)
    sequence.edit(next_dict=next_dict)

  def stepCheckConfigureWebSiteForm(self, sequence=None, sequence_list=None, **kw):
    """ Check the installation form """
    response_dict = sequence.get("response_dict")
    # configuration is finished. We are at the Install state.
    self.assertEquals('show', response_dict['command'])
    self.assertEquals('Previous', response_dict['previous'])
    self.assertEquals('Configure Web Site', response_dict['next'])

  def stepSetupWebSiteConfiguration(self, sequence=None, sequence_list=None, **kw):
    """ """
    next_dict = dict(your_default_available_language="pt-BR")
    sequence.edit(next_dict=next_dict)

  def stepCheckConfigureInstallationForm(self, sequence=None, sequence_list=None, **kw):
    """ Check the installation form """
    response_dict = sequence.get("response_dict")
    self.assertEquals('show', response_dict['command'])
    self.assertEquals('Previous', response_dict['previous'])
    self.assertEquals('Install', response_dict['next'])

  def stepSetupInstallConfiguration(self, sequence=None, sequence_list=None, **kw):
    """ Install the Configuration """
    sequence.edit(next_dict={})

  def stepCheckInstallConfiguration(self, sequence=None, sequence_list=None, **kw):
    """ Check the installation of the configuration """
    response_dict = sequence.get("response_dict")
    self.assertEquals('install', response_dict['command'])

  def stepStartConfigurationInstallation(self, sequence=None, sequence_list=None, **kw):
    """ Starts the installation """
    business_configuration = sequence.get("business_configuration")
    self.portal.portal_configurator.startInstallation(
         business_configuration, REQUEST=self.portal.REQUEST)

  def stepCheckUNGWebSiteAfterInstallation(self, sequence=None, sequence_list=None, **kw):
    """ Check if UNG Web Site is published and your language"""
    self.assertEquals(self.portal.web_site_module.ung.getValidationState(),
                      "published")
    self.assertEquals(self.portal.web_site_module.ung.getDefaultAvailableLanguage(),
                      "pt-BR")

  def test_standard_workflow_brazil(self):
    """ Test the standard workflow with brazilian configuration """
    sequence_list = SequenceList()
    sequence_list.addSequenceString(self.DEFAULT_SEQUENCE_LIST)
    sequence_list.play(self)