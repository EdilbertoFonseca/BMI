# -*- coding: UTF-8 -*-

"""
Description: GUI dialogs for the BMI calculator add-on.
"""

# Author: Edilberto Fonseca
# Email: <edilberto.fonseca@outlook.com>
# Copyright (C) 2025 Edilberto Fonseca
# This file is covered by the GNU General Public License.
# See the file COPYING for more details or visit https://www.gnu.org/licenses/gpl-2.0.html.

# Date of creation 11/08/2022.

import addonHandler
import wx
import gui
from gui import guiHelper

from datetime import datetime

from .bmi_calculator import validate_inputs, calculate_bmi
from .history_manager import save_to_history, load_history

# Initialize translation support
addonHandler.initTranslation()

class BMIDialog(wx.Dialog):
	"""Main dialog for BMI calculation."""

	_instance = None

	def __new__(cls, *args, **kwargs):
		if not cls._instance:
			cls._instance = super(BMIDialog, cls).__new__(cls, *args, **kwargs)
		return cls._instance

	def __init__(self, parent, title):
		if hasattr(self, "initialized"):
			return
		self.initialized = True

		WIDTH = 450
		HEIGHT = 180

		super(BMIDialog, self).__init__(parent, title=title, size=(WIDTH, HEIGHT))
		panel = wx.Panel(self)
		main_sizer = wx.BoxSizer(wx.VERTICAL)
		field_helper = guiHelper.BoxSizerHelper(panel, wx.VERTICAL)
		button_helper = guiHelper.BoxSizerHelper(panel, wx.HORIZONTAL)

		self.heightCtrl = field_helper.addLabeledControl(
			_("Enter or select your height in centimeters:"), wx.SpinCtrl
		)
		self.heightCtrl.SetRange(1, 250)

		self.weightCtrl = field_helper.addLabeledControl(
			_("Enter or select your weight in kilograms:"), wx.SpinCtrl
		)
		self.weightCtrl.SetRange(1, 500)

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

		main_sizer.Add(field_helper.sizer, border=10, flag=wx.ALL)
		main_sizer.Add(button_helper.sizer, border=5, flag=wx.CENTER)
		panel.SetSizerAndFit(main_sizer)

	def on_calculate(self, event):
		"""Handles BMI calculation and shows the result dialog."""

		height = self.heightCtrl.GetValue()
		weight = self.weightCtrl.GetValue()

		validation_msg = validate_inputs(height, weight)
		if validation_msg:
			gui.messageBox(validation_msg, _("Attention"), wx.ICON_ERROR)
			self.heightCtrl.SetFocus()
			return

		bmi = calculate_bmi(height / 100, weight)
		bmi_formatted = "{:.1f}".format(bmi)

		min_weight = round(18.5 * ((height / 100) ** 2), 1)
		max_weight = round(24.9 * ((height / 100) ** 2), 1)
		ideal_range = _("Ideal weight range for your height: {} kg to {} kg.").format(min_weight, max_weight)

		observation = _(
			"Observation:\n\n"
			"For an accurate interpretation of BMI, it is important to consider other factors such as "
			"body composition, fat distribution, age, gender, and overall health.\n"
			"It is always recommended to consult a healthcare professional for proper guidance on health and weight."
		)

		if bmi < 18.5:
			msg = _("""Your BMI is {}.\n\nYou are underweight.\n\nIt is important to consult a doctor or nutritionist to identify healthy ways to gain weight.\n\n{}\n\n{}""").format(bmi_formatted, observation, ideal_range)
		elif 18.5 <= bmi < 25:
			msg = _("""Your BMI is {}.\n\nYou are at a healthy weight.\n\nMaintain it with a balanced diet and regular physical activity.\n\n{}\n\n{}""").format(bmi_formatted, observation, ideal_range)
		elif 25 <= bmi < 30:
			msg = _("""Your BMI is {}.\n\nYou are overweight.\n\nIt is important to consult a doctor or nutritionist to identify healthy weight loss strategies.\n\n{}\n\n{}""").format(bmi_formatted, observation, ideal_range)
		elif 30 <= bmi < 40:
			msg = _("""Your BMI is {}.\n\nYou are significantly overweight.\n\nPlease consult a healthcare provider for guidance.\n\n{}\n\n{}""").format(bmi_formatted, observation, ideal_range)
		else:
			msg = _("""Your BMI is {}.\n\nYour BMI indicates that you are in the obese range.\n\nIt is important to consult a doctor to reduce health risks through safe weight loss.\n\n{}\n\n{}""").format(bmi_formatted, observation, ideal_range)

		save_to_history(height, weight, bmi)
		gui.messageBox(msg, _("Attention"), wx.ICON_INFORMATION)
		self.on_clear(event)

	def on_clear(self, event):
		"""Clears the input fields."""
		self.heightCtrl.SetValue(1)
		self.weightCtrl.SetValue(1)
		self.heightCtrl.SetFocus()

	def on_cancel(self, event):
		"""Closes the dialog."""
		self.Destroy()

	def on_show_history(self, event):
		"""Displays the last 10 BMI calculations."""
		history = load_history()
		if not history:
			gui.messageBox(_("No history found."), _("History"), wx.ICON_INFORMATION)
			return

		last_entries = history[-10:]
		result = _("Last 10 BMI calculations:\n\n")
		for record in last_entries:
			dt = datetime.fromisoformat(record["timestamp"])
			formatted_dt = dt.strftime("%d/%m/%Y %H:%M")
			result += _("Date: {} | Height: {} cm | Weight: {} kg | BMI: {}\n").format(
				formatted_dt, record["height"], record["weight"], record["bmi"]
			)

		dlg = TextDisplayDialog(None, _("History"), result)
		gui.mainFrame.prePopup()
		dlg.CentreOnScreen()
		dlg.ShowModal()
		dlg.Destroy()
		gui.mainFrame.postPopup()


class TextDisplayDialog(wx.Dialog):
	"""Reusable dialog to display long or multiline text."""

	def __init__(self, parent, title="Display text", content=""):
		super().__init__(parent, title=title, size=(500, 300))

		main_sizer = wx.BoxSizer(wx.VERTICAL)

		self.text_ctrl = wx.TextCtrl(
			self,
			value=content,
			style=wx.TE_MULTILINE | wx.TE_READONLY | wx.HSCROLL | wx.VSCROLL
		)
		main_sizer.Add(self.text_ctrl, proportion=1, flag=wx.EXPAND | wx.ALL, border=10)

		btn_sizer = self.CreateButtonSizer(wx.OK)
		main_sizer.Add(btn_sizer, flag=wx.ALIGN_CENTER | wx.ALL, border=10)

		self.SetSizer(main_sizer)
		self.Centre()
