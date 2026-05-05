# -*- coding: UTF-8 -*-

"""
Author: Edilberto Fonseca <edilberto.fonseca@outlook.com>
Copyright: (C) 2025 - 2026 Edilberto Fonseca

This file is covered by the GNU General Public License.
See the file COPYING for more details or visit:
https://www.gnu.org/licenses/gpl-2.0.html

-------------------------------------------------------------------------
AI DISCLOSURE / NOTA DE IA:
This project utilizes AI for code refactoring and logic suggestions.
All AI-generated code was manually reviewed and tested by the author.
-------------------------------------------------------------------------

Created on: 11/08/2022.
"""

import addonHandler
import globalPluginHandler
import globalVars
import gui
import wx
from logHandler import log
from scriptHandler import script

from .main import BMIDialog

# Get the add-on summary from the manifest
ADDON_SUMMARY = addonHandler.getCodeAddon().manifest["summary"]

# Initialize translation support
addonHandler.initTranslation()


def disableInSecureMode(decorated_cls):
	"""Disables the plugin if NVDA is in secure mode."""
	if globalVars.appArgs.secure:
		return globalPluginHandler.GlobalPlugin
	return decorated_cls


@disableInSecureMode
class GlobalPlugin(globalPluginHandler.GlobalPlugin):
	"""Global plugin to add the BMI calculator to the Tools menu and shortcut system."""

	def __init__(self):
		"""Constructor for the global plugin."""
		super(GlobalPlugin, self).__init__()
		self.toolsMenu = gui.mainFrame.sysTrayIcon.toolsMenu

		# Translators: Add-on title in the Tools menu.
		self.menuItem = self.toolsMenu.Append(
			wx.ID_ANY,
			_("&Calculate your BMI..."),
		)
		gui.mainFrame.sysTrayIcon.Bind(
			wx.EVT_MENU,
			self.script_onBMIDialog,
			self.menuItem,
		)

	@script(
		gesture="kb:Windows+alt+I",
		# Translators: Text displayed in NVDA's input gesture dialog.
		description=_("BMI - This add-on calculates the Body Mass Index."),
		category=ADDON_SUMMARY,
	)
	def script_onBMIDialog(self, gesture):
		"""Triggered by shortcut or menu item to display the BMI dialog."""
		wx.CallAfter(self.onBMIDialog)

	def onBMIDialog(self):
		"""Displays the BMI calculation dialog."""
		dlg = BMIDialog(gui.mainFrame, _("Calculation of the Body Mass Index."))
		gui.mainFrame.prePopup()
		dlg.CentreOnScreen()
		dlg.Show()
		gui.mainFrame.postPopup()

	def terminate(self):
		"""Removes the Tools menu entry when the add-on is unloaded."""
		try:
			self.toolsMenu.Remove(self.menuItem)
		except Exception as e:
			log.error("Error removing menu item 'Calculate your BMI...': %s", e)
