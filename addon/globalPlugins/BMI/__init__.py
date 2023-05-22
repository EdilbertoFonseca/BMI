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

# Imports from the IMC module.
from .main import DialogBMI

# Module required to carry out the translations.
addonHandler.initTranslation()

def avoidSecure():
	# Avoid use in secure screens and during installation
	if (globalVars.appArgs.secure or globalVars.appArgs.install or globalVars.appArgs.minimal):
		return


class GlobalPlugin(globalPluginHandler.GlobalPlugin):

	# Creating the constructor of the newly created GlobalPlugin class.
	def __init__(self, *args, **kwargs):
		super(GlobalPlugin, self).__init__(*args, **kwargs)
		# Avoid use in secure screens
		if globalVars.appArgs.secure:
			return

		self.toolsMenu = gui.mainFrame.sysTrayIcon.toolsMenu

		# Translators: Add-on title in the tools menu.
		self.calculate = self.toolsMenu.Append(-1, _("&Calculate your BMI"))
		gui.mainFrame.sysTrayIcon.Bind(
			wx.EVT_MENU, self.script_onIMC, self.calculate)

	#defining a script with decorator:
	@script(
		gesture="kb:Windows+alt+I",
		description=_("BMI, This add-on calculates the body mass index.")
	)
	def script_onIMC(self, gesture):
		# Translators: Dialog title Body mass Index Calculation.
		self.dlg = DialogBMI(gui.mainFrame, _(
			"Calculation of the Body mass Index."))
		gui.mainFrame.prePopup()
		self.dlg.Show()
		self.dlg.CentreOnScreen()
		gui.mainFrame.postPopup()

		# This terminate function is necessary when creating new menus.
	def terminate(self):
		try:
			if wx.version().startswith("4"):
				self.toolsMenu.Remove(self.calculate)
			else:
				self.toolsMenu.RemoveItem(self.calculate)
		except:
			pass
