# -*- coding: UTF-8 -*-

"""
Author: Edilberto Fonseca <edilberto.fonseca@outlook.com>
Copyright: (C) 2025 Edilberto Fonseca

This file is covered by the GNU General Public License.
See the file COPYING for more details or visit:
https://www.gnu.org/licenses/gpl-2.0.html

Created on: 11/08/2022.
"""

import addonHandler
import globalPluginHandler
import globalVars
import gui
import wx
from logHandler import log
from scriptHandler import script

# Import function that displays the dialog (now modal)
from .main import show_bmi_dialog

# Initialize translation support
addonHandler.initTranslation()

# Load add-on summary (for Input Gestures dialog localization)
ADDON_SUMMARY = addonHandler.getCodeAddon().manifest["summary"]


def disable_in_secure_mode(cls):
	"""
	Decorator that disables the plugin entirely in NVDA Secure Mode.
	Necessário para impedir que janelas ou scripts sejam executados
	em ambientes restritos, conforme o guia de desenvolvimento.
	"""
	if globalVars.appArgs.secure:
		return globalPluginHandler.GlobalPlugin
	return cls


@disable_in_secure_mode
class GlobalPlugin(globalPluginHandler.GlobalPlugin):
	"""
	Global plugin que adiciona o item 'Calculate BMI' ao menu Ferramentas
	e registra o atalho global configurado.
	"""

	def __init__(self):
		super().__init__()

		# Localização robusta do menu Ferramentas
		try:
			self.tools_menu = gui.mainFrame.sysTrayIcon.toolsMenu
		except Exception as error:
			log.error(f"BMI Add-on: Tools menu not found: {error}")
			return

		# Criar o item do menu
		self.menu_item = self.tools_menu.Append(
			wx.ID_ANY,
			_("&Calculate your BMI...")
		)

		# Vincular ação ao item
		gui.mainFrame.sysTrayIcon.Bind(
			wx.EVT_MENU,
			self.script_open_bmi_dialog,
			self.menu_item
		)

	@script(
		gesture="kb:Windows+Alt+I",
		description=_("BMI - Opens the Body Mass Index calculator."),
		category=ADDON_SUMMARY
	)
	def script_open_bmi_dialog(self, gesture):
		"""Invoked by menu or gesture to open the BMI dialog."""
		wx.CallAfter(show_bmi_dialog)

	def terminate(self):
		"""
		Remove o item de menu ao descarregar o add-on, conforme
		solicitado pelo guia de desenvolvimento do NVDA.
		"""
		try:
			if hasattr(self, "tools_menu") and self.menu_item:
				self.tools_menu.Remove(self.menu_item)
		except Exception as error:
			log.error(f"Failed to remove BMI menu item: {error}")
