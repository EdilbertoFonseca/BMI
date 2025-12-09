# -*- coding: UTF-8 -*-

"""
Author: Edilberto Fonseca <edilberto.fonseca@outlook.com>
Copyright: (C) 2025 Edilberto Fonseca

This file is covered by the GNU General Public License.
See the file COPYING for more details or visit:
https://www.gnu.org/licenses/gpl-2.0.html

Created on: 11/08/2022
"""

import addonHandler
import globalVars
import gui
import ui

from .dialogs import BMIDialog

# Load add-on summary (for dialog localization)
ADDON_SUMMARY = addonHandler.getCodeAddon().manifest["summary"]

_isDialogOpen = False  # Flag to track if the dialog is already open

# Initialize translation support for this module
addonHandler.initTranslation()

def show_bmi_dialog():
	"""
	Displays the BMI calculation dialog as a modal window.

	This function implements the recommended NVDA workflow for opening dialogs:
	1. Call gui.mainFrame.prePopup() before showing the dialog
	   to notify NVDA that the focus will temporarily move.
	2. Show the dialog in modal form using ShowModal().
	3. Destroy the dialog after closing to free resources.
	4. Call gui.mainFrame.postPopup() to restore normal focus behavior.

	Also prevents dialog execution in Secure Mode, in accordance with
	NVDA’s add-on security guidelines.
	"""
	global _isDialogOpen
	if _isDialogOpen:
		ui.message(_("An instance of {} is already open.").format(ADDON_SUMMARY))
		return
	_isDialogOpen = True

	# Block dialog execution in NVDA Secure Mode for safety
	if globalVars.appArgs.secure:
		return

	dlg = BMIDialog(gui.mainFrame, _("Calculation of the Body Mass Index."))

	gui.mainFrame.prePopup()
	dlg.CentreOnScreen()

	dlg.ShowModal()

	try:
		dlg.Destroy()
	except RuntimeError:
		pass

	gui.mainFrame.postPopup()
	_isDialogOpen = False
