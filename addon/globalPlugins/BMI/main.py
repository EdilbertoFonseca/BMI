# -*- coding: UTF-8 -*-

"""
Description: Main entry point to open the BMI calculation dialog.
"""

# Author: Edilberto Fonseca
# Email: <edilberto.fonseca@outlook.com>
# Copyright (C) 2025 Edilberto Fonseca
# This file is covered by the GNU General Public License.
# See the file COPYING for more details or visit https://www.gnu.org/licenses/gpl-2.0.html.

# Date of creation 11/08/2022.

import addonHandler
import gui
from .dialogs import BMIDialog

# Initialize translation support
addonHandler.initTranslation()

def show_bmi_dialog():
	"""Displays the BMI calculation dialog."""
	dlg = BMIDialog(gui.mainFrame, _("Calculation of the Body Mass Index."))
	gui.mainFrame.prePopup()
	dlg.CentreOnScreen()
	dlg.Show()
	gui.mainFrame.postPopup()
