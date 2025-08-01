# -*- coding: UTF-8 -*-

"""
 Description: NVDA Add-on initialization for the BMI calculator.

 This file integrates the add-on into NVDA, adding a menu item,
 keyboard shortcut, and secure-mode check.
"""

# Author: Edilberto Fonseca
# Email: <edilberto.fonseca@outlook.com>
# Copyright (C) 2025 Edilberto Fonseca
# This file is covered by the GNU General Public License.
# See the file COPYING for more details or visit https://www.gnu.org/licenses/gpl-2.0.html.

# Date of creation 11/08/2022.

import addonHandler
import globalPluginHandler
import globalVars
import gui
import wx
from logHandler import log
from scriptHandler import script

# Import the dialog display function
from .main import show_bmi_dialog

# Get the add-on summary from the manifest
ADDON_SUMMARY = addonHandler.getCodeAddon().manifest["summary"]

# Initialize translation support
addonHandler.initTranslation()


def disable_in_secure_mode(decorated_cls):
	"""Disables the plugin if NVDA is in secure mode."""
	if globalVars.appArgs.secure:
		return globalPluginHandler.GlobalPlugin
	return decorated_cls


@disable_in_secure_mode
class GlobalPlugin(globalPluginHandler.GlobalPlugin):
	"""Global plugin to add the BMI calculator to the Tools menu and shortcut system."""

	def __init__(self):
		"""Constructor for the global plugin."""
		super(GlobalPlugin, self).__init__()
		self.tools_menu = gui.mainFrame.sysTrayIcon.toolsMenu

		# Translators: Add-on title in the Tools menu.
		self.menu_item = self.tools_menu.Append(
			wx.ID_ANY, _("&Calculate your BMI...")
		)
		gui.mainFrame.sysTrayIcon.Bind(
			wx.EVT_MENU, self.script_on_bmi_dialog, self.menu_item
		)

	@script(
		gesture="kb:Windows+alt+I",
		# Translators: Text displayed in NVDA's input gesture dialog.
		description=_("BMI - This add-on calculates the Body Mass Index."),
		category=ADDON_SUMMARY
	)
	def script_on_bmi_dialog(self, gesture):
		"""Triggered by shortcut or menu item to display the BMI dialog."""
		show_bmi_dialog()

	def terminate(self):
		"""Removes the Tools menu entry when the add-on is unloaded."""
		try:
			self.tools_menu.Remove(self.menu_item)
		except Exception as e:
			log.error("Error removing menu item 'Calculate your BMI...': %s", e)
