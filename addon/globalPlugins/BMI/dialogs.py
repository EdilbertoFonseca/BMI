# -*- coding: UTF-8 -*-

"""
Author: Edilberto Fonseca <edilberto.fonseca@outlook.com>
Copyright: (C) 2025 Edilberto Fonseca

This file is covered by the GNU General Public License.
See the file COPYING for more details or visit:
https://www.gnu.org/licenses/gpl-2.0.html

Created on: 11/08/2022
"""

from datetime import datetime

import addonHandler
import gui
import wx
from gui import guiHelper

from .bmi_calculator import calculate_bmi, validate_inputs
from .history_manager import load_history, save_to_history

# Initialize translation for this module
addonHandler.initTranslation()


class BMIDialog(wx.Dialog):
	"""
	Main dialog used to input height and weight and calculate the BMI.
	"""

	def __init__(self, parent, title):
		"""Create and configure the BMI calculator dialog."""
		if hasattr(self, "initialized"):
			return
		self.initialized = True

		super().__init__(parent, title=title)

		panel = wx.Panel(self)
		main_sizer = wx.BoxSizer(wx.VERTICAL)

		# Helpers for labeled fields and horizontal button arrangement
		field_helper = guiHelper.BoxSizerHelper(panel, wx.VERTICAL)
		button_helper = guiHelper.BoxSizerHelper(panel, wx.HORIZONTAL)

		# Height input (centimeters)
		self.heightCtrl = field_helper.addLabeledControl(
			_("Enter or select your height in centimeters:"),
			wx.SpinCtrl
		)
		self.heightCtrl.SetRange(1, 250)
		self.heightCtrl.SetValue(170)

		# Weight input (kilograms)
		self.weightCtrl = field_helper.addLabeledControl(
			_("Enter or select your weight in kilograms:"),
			wx.SpinCtrl
		)
		self.weightCtrl.SetRange(1, 500)
		self.weightCtrl.SetValue(70)

		# --- Buttons ---
		self.calcButton = button_helper.addItem(
			wx.Button(panel, -1, label=_("C&alculate"))
		)
		self.Bind(wx.EVT_BUTTON, self.on_calculate, self.calcButton)

		self.clearButton = button_helper.addItem(
			wx.Button(panel, -1, label=_("C&lear"))
		)
		self.Bind(wx.EVT_BUTTON, self.on_clear, self.clearButton)

		self.historyButton = button_helper.addItem(
			wx.Button(panel, -1, label=_("&History"))
		)
		self.Bind(wx.EVT_BUTTON, self.on_show_history, self.historyButton)

		self.cancelButton = button_helper.addItem(
			wx.Button(panel, wx.ID_CANCEL, label=_("&Cancel"))
		)
		self.Bind(wx.EVT_BUTTON, self.on_cancel, id=wx.ID_CANCEL)

		# Add everything to the dialog layout
		main_sizer.Add(field_helper.sizer, flag=wx.ALL, border=10)
		main_sizer.Add(button_helper.sizer, flag=wx.ALL | wx.CENTER, border=10)

		panel.SetSizerAndFit(main_sizer)
		self.Fit()
		self.Layout()

	# -------------------------
	# Button event handlers
	# -------------------------

	def on_calculate(self, event):
		"""
		Perform BMI calculation, validate inputs, display results and
		save the record in history.
		"""

		height = self.heightCtrl.GetValue()
		weight = self.weightCtrl.GetValue()

		# Validation (height in cm, weight in kg)
		validation_msg = validate_inputs(height / 100, weight)
		if validation_msg:
			gui.messageBox(validation_msg, _("Attention"), wx.ICON_ERROR)
			self.heightCtrl.SetFocus()
			return

		# Perform BMI calculation (height must be in meters)
		bmi_value = calculate_bmi(height / 100, weight)
		bmi_formatted = f"{bmi_value:.1f}"

		# Ideal weight range calculation
		min_weight = round(18.5 * ((height / 100) ** 2), 1)
		max_weight = round(24.9 * ((height / 100) ** 2), 1)
		ideal_range = _(
			"Ideal weight range for your height: {} kg to {} kg."
		).format(min_weight, max_weight)

		# Common observation text
		observation = _(
			"Observation:\n\n"
			"For accurate BMI interpretation, several factors must be considered, "
			"including body composition, fat distribution, age, gender, and overall health.\n"
			"Consulting a healthcare professional is recommended for proper guidance."
		)

		# BMI category messages
		if bmi_value < 18.5:
			category = _("You are underweight.")
		elif 18.5 <= bmi_value < 25:
			category = _("You are at a healthy weight.")
		elif 25 <= bmi_value < 30:
			category = _("You are overweight.")
		elif 30 <= bmi_value < 40:
			category = _("You are significantly overweight.")
		else:
			category = _("Your BMI indicates obesity.")

		msg = _(
			"Your BMI is {}.\n\n{}\n\n{}\n\n{}"
		).format(bmi_formatted, category, observation, ideal_range)

		# Save to history
		save_to_history(height, weight, bmi_value)

		# Display result
		gui.messageBox(msg, _("Attention"), wx.ICON_INFORMATION)

		# Clear fields for next use
		self.on_clear(event)

	def on_clear(self, event):
		"""Reset height and weight fields to default values."""
		self.heightCtrl.SetValue(170)
		self.weightCtrl.SetValue(70)
		self.heightCtrl.SetFocus()

	def on_cancel(self, event):
		"""Close the dialog."""
		self.EndModal(wx.ID_CANCEL)

	def on_show_history(self, event):
		"""
		Load BMI history and display it using the TextDisplayDialog.
		Shows only the last 10 records.
		"""
		history = load_history() or []

		if not history:
			gui.messageBox(_("No history found."), _("History"), wx.ICON_INFORMATION)
			return

		last_entries = history[-10:]

		result = _("Last 10 BMI calculations:\n\n")
		for record in last_entries:
			dt = datetime.fromisoformat(record["timestamp"])
			formatted_dt = dt.strftime("%d/%m/%Y %H:%M")
			result += _(
				"Date: {} | Height: {} cm | Weight: {} kg | BMI: {}\n"
			).format(
				formatted_dt, record["height"], record["weight"], record["bmi"]
			)

		dlg = TextDisplayDialog(gui.mainFrame, _("History"), result)

		gui.mainFrame.prePopup()
		dlg.CentreOnScreen()
		dlg.ShowModal()
		dlg.Destroy()
		gui.mainFrame.postPopup()


class TextDisplayDialog(wx.Dialog):
	"""
	Simple reusable dialog for presenting long or multiline text.

	Used for showing calculation history or other informational content.
	"""

	def __init__(self, parent, title="Display text", content=""):
		super().__init__(parent, title=title, size=(500, 300))

		main_sizer = wx.BoxSizer(wx.VERTICAL)

		# Multiline read-only text field
		self.text_ctrl = wx.TextCtrl(
			self,
			value=content,
			style=wx.TE_MULTILINE | wx.TE_READONLY | wx.HSCROLL | wx.VSCROLL
		)
		main_sizer.Add(self.text_ctrl, proportion=1,
			flag=wx.EXPAND | wx.ALL, border=10)

		# OK button (default close action)
		btn_sizer = self.CreateButtonSizer(wx.OK)
		main_sizer.Add(btn_sizer, flag=wx.ALIGN_CENTER | wx.ALL, border=10)

		self.SetSizer(main_sizer)
		self.Centre()
