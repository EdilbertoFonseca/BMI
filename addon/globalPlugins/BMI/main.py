# -*- coding: UTF-8 -*-

"""
Main entry point to open the BMI calculation dialog.
"""

import addonHandler
import gui
from .dialogs import BMIDialog

# Initializes the translation
addonHandler.initTranslation()

def show_bmi_dialog():
	"""Displays the BMI calculation dialog."""
	dlg = BMIDialog(gui.mainFrame, _("Calculation of the Body Mass Index."))
	gui.mainFrame.prePopup()
	dlg.CentreOnScreen()
	dlg.Show()
	gui.mainFrame.postPopup()
