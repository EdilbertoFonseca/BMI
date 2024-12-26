# -*- coding: UTF-8 -*-

# Description:
# Calculate your body mass with this add-on.

# Thanks:
# Special thanks to the contributors Rui Fonte, Noelia and Dalen
# who have helped make this version possible.

# Author: Edilberto Fonseca
# Email: <edilberto.fonseca@outlook.com>
# Copyright (C) 2022-2025 Edilberto Fonseca
# This file is covered by the GNU General Public License.
# See the file COPYING for more details or visit https://www.gnu.org/licenses/gpl-2.0.html.

# Creation date: 08/11/2022.

# Standard NVDA imports.
import logging

import addonHandler
import globalPluginHandler
import globalVars
import gui
import wx
from scriptHandler import script

# Imports from the BMI module.
from .main import DialogBMI

# Configuring the log
logging.basicConfig(level=logging.ERROR)

# Get the add-on summary contained in the manifest.
ADDON_SUMMARY = addonHandler.getCodeAddon().manifest["summary"]

# Initializes the translation
addonHandler.initTranslation()


def disableInSecureMode(decoratedCls):
	"""
	Decorator to disable the plugin in secure mode.
	"""
	if globalVars.appArgs.secure:
		return globalPluginHandler.GlobalPlugin
	return decoratedCls


@disableInSecureMode
class GlobalPlugin(globalPluginHandler.GlobalPlugin):

	# Creating the constructor of the newly created GlobalPlugin class.
	def __init__(self):
		super(GlobalPlugin, self).__init__()
		self.toolsMenu = gui.mainFrame.sysTrayIcon.toolsMenu

		# Translators: Add-on title in the tools menu.
		self.calculate = self.toolsMenu.Append(
			wx.ID_ANY, _("&Calculate your BMI..."))
		gui.mainFrame.sysTrayIcon.Bind(
			wx.EVT_MENU, self.script_onBMI, self.calculate)

	# defining a script with decorator:
	@script(
		gesture="kb:Windows+alt+I",
		# Translators: Text displayed in NVDA help.
		description=_("BMI, This add-on calculates the body mass index."),
		category=ADDON_SUMMARY
	)
	def script_onBMI(self, gesture):
		# Translators: Dialog title Body mass Index Calculation.
		self.dlg = DialogBMI(gui.mainFrame, _(
			"Calculation of the Body mass Index."))
		gui.mainFrame.prePopup()
		self.dlg.Show()
		self.dlg.CentreOnScreen()
		gui.mainFrame.postPopup()

	def terminate(self):
		"""
		This terminate function is necessary when creating new menus.
		"""
		try:
			self.toolsMenu.Remove(self.calculate)
		except Exception as e:
			logging.error("Error removing menu option 'Calculate your BMI...': %s", e)
