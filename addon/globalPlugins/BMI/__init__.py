# -*- coding: UTF-8 -*-

# Calculate your body mass with this add-on.
# Author: Edilberto Fonseca.
# Thanks: To Rui Fontes, for his collaboration and guidance during the development of the addon.
# Creation date: 08/11/2022.

# Standard NVDA imports.
import globalPluginHandler
import addonHandler
from scriptHandler import script
import gui
import globalVars
import wx

# Imports from the BMI module.
from .main import DialogBMI

# Get the add-on summary contained in the manifest.
ADDON_SUMMARY = addonHandler.getCodeAddon().manifest["summary"]

# Module required to carry out the translations.
addonHandler.initTranslation()

def disableInSecureMode(decoratedCls):
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
		self.calculateBMI = self.toolsMenu.Append(wx.ID_ANY, _("&Calculate your BMI..."))
		gui.mainFrame.sysTrayIcon.Bind(
			wx.EVT_MENU, self.script_activateBMI, self.calculateBMI)

	def onBMI(self, evt):
		# Translators: Dialog title Body mass Index Calculation.
		self.dlg = DialogBMI(gui.mainFrame, _(
			"Calculation of the Body mass Index."))
		gui.mainFrame.prePopup()
		self.dlg.Show()
		self.dlg.CentreOnScreen()
		gui.mainFrame.postPopup()

	#defining a script with decorator:
	@script(
		gesture="kb:Windows+alt+I",

		# Translators: Text displayed in NVDA help.
		description=_("BMI, This add-on calculates the body mass index."),
		category=ADDON_SUMMARY
	)
	def script_activateBMI(self, gesture):
		wx.CallAfter(self.onBMI, None)

	# This terminate function is necessary when creating new menus.
	def terminate(self):
		try:
			self.toolsMenu.Remove(self.calculateBMI)
		except Exception:
			pass
