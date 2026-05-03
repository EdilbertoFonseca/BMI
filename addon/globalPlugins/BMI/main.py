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

from datetime import datetime

import addonHandler
import gui
import wx
from gui import guiHelper

from .bmiCalculator import calculate, validateInputs
from .historyManager import loadHistory, saveToHistory

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
		mainSizer = wx.BoxSizer(wx.VERTICAL)
		fieldHelper = guiHelper.BoxSizerHelper(panel, wx.VERTICAL)
		buttonHelper = guiHelper.BoxSizerHelper(panel, wx.HORIZONTAL)

		self.heightCtrl = fieldHelper.addLabeledControl(
			# translator: Label for height input field
			_("Enter or select your height in centimeters:"),
			wx.SpinCtrl,
		)
		self.heightCtrl.SetRange(1, 250)

		self.weightCtrl = fieldHelper.addLabeledControl(
			# translator: Label for weight input field
			_("Enter or select your weight in kilograms:"),
			wx.SpinCtrl,
		)
		self.weightCtrl.SetRange(1, 500)

		self.buttonCalc = buttonHelper.addItem(
			wx.Button(panel, -1, label=_("C&alculate")),
		)
		self.Bind(wx.EVT_BUTTON, self.onCalculate, self.buttonCalc)

		self.buttonClear = buttonHelper.addItem(
			wx.Button(panel, -1, label=_("C&lear")),
		)
		self.Bind(wx.EVT_BUTTON, self.onClear, self.buttonClear)

		self.buttonHistory = buttonHelper.addItem(
			wx.Button(panel, -1, label=_("&History")),
		)
		self.Bind(wx.EVT_BUTTON, self.onShowHistory, self.buttonHistory)

		self.buttonCancel = buttonHelper.addItem(
			wx.Button(panel, wx.ID_CANCEL, label=_("&Cancel")),
		)
		self.Bind(wx.EVT_BUTTON, self.onCancel, id=wx.ID_CANCEL)

		mainSizer.Add(fieldHelper.sizer, border=10, flag=wx.ALL)
		mainSizer.Add(buttonHelper.sizer, border=5, flag=wx.CENTER)
		panel.SetSizerAndFit(mainSizer)

	def onCalculate(self, event):
		"""Handles BMI calculation and shows the result dialog."""

		height = self.heightCtrl.GetValue()
		weight = self.weightCtrl.GetValue()

		validationMsg = validateInputs(height, weight)
		if validationMsg:
			gui.messageBox(validationMsg, _("Attention"), wx.ICON_ERROR)
			self.heightCtrl.SetFocus()
			return

		bmi = calculate(height / 100, weight)

		if bmi is None:
			gui.messageBox(
				# translator: Error message when BMI calculation fails
				_("Unable to calculate BMI. Please check the values."),
				_("Attention"),
				wx.ICON_ERROR,
			)
			return

		bmiFormatted = "{:.1f}".format(bmi)

		minWeight = round(18.5 * ((height / 100) ** 2), 1)
		maxWeight = round(24.9 * ((height / 100) ** 2), 1)
		idealRange = _("Ideal weight range for your height: {} kg to {} kg.").format(minWeight, maxWeight)

		# translator: General observation about BMI results, shown in the result dialog.
		observation = _(
			"Observation:\n\n"
			+ "For an accurate interpretation of BMI, it is important to consider other factors such as "
			+ "body composition, fat distribution, age, gender, and overall health.\n"
			+ "It is always recommended to consult a healthcare professional for proper guidance on health and weight.",
		)

		if bmi < 18.5:
			msg = _(
				"""Your BMI is {}.\n\nYou are underweight.\n\nIt is important to consult a doctor or nutritionist to identify healthy ways to gain weight.\n\n{}\n\n{}""",
			).format(bmiFormatted, observation, idealRange)
		elif 18.5 <= bmi < 25:
			msg = _(
				"""Your BMI is {}.\n\nYou are at a healthy weight.\n\nMaintain it with a balanced diet and regular physical activity.\n\n{}\n\n{}""",
			).format(bmiFormatted, observation, idealRange)
		elif 25 <= bmi < 30:
			msg = _(
				"""Your BMI is {}.\n\nYou are overweight.\n\nIt is important to consult a doctor or nutritionist to identify healthy weight loss strategies.\n\n{}\n\n{}""",
			).format(bmiFormatted, observation, idealRange)
		elif 30 <= bmi < 40:
			msg = _(
				"""Your BMI is {}.\n\nYou are significantly overweight.\n\nPlease consult a healthcare provider for guidance.\n\n{}\n\n{}""",
			).format(bmiFormatted, observation, idealRange)
		else:
			msg = _(
				"""Your BMI is {}.\n\nYour BMI indicates that you are in the obese range.\n\nIt is important to consult a doctor to reduce health risks through safe weight loss.\n\n{}\n\n{}""",
			).format(bmiFormatted, observation, idealRange)

		saveToHistory(height, weight, bmi)
		gui.messageBox(msg, _("Attention"), wx.ICON_INFORMATION)
		self.onClear(event)

	def onClear(self, event):
		"""Clears the input fields."""
		self.heightCtrl.SetValue(1)
		self.weightCtrl.SetValue(1)
		self.heightCtrl.SetFocus()

	def onCancel(self, event):
		"""Closes the dialog."""
		self.Destroy()

	def onShowHistory(self, event):
		"""Displays the last 10 BMI calculations."""
		history = loadHistory()
		if not history:
			# translator: Message shown when there is no BMI calculation history available.
			gui.messageBox(_("No history found."), _("History"), wx.ICON_INFORMATION)
			return

		lastEntries = history[-10:]
		result = _("Last 10 BMI calculations:\n\n")
		for record in lastEntries:
			dt = datetime.fromisoformat(record["timestamp"])
			formattedDT = dt.strftime("%d/%m/%Y %H:%M")
			result += _("Date: {} | Height: {} cm | Weight: {} kg | BMI: {}\n").format(
				formattedDT,
				record["height"],
				record["weight"],
				record["bmi"],
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

		mainSizer = wx.BoxSizer(wx.VERTICAL)

		self.textCtrl = wx.TextCtrl(
			self,
			value=content,
			style=wx.TE_MULTILINE | wx.TE_READONLY | wx.HSCROLL | wx.VSCROLL,
		)
		mainSizer.Add(self.textCtrl, proportion=1, flag=wx.EXPAND | wx.ALL, border=10)

		buttonSizer = self.CreateButtonSizer(wx.OK)
		mainSizer.Add(buttonSizer, flag=wx.ALIGN_CENTER | wx.ALL, border=10)

		self.SetSizer(mainSizer)
		self.Centre()
