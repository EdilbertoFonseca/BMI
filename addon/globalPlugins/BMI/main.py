# -*- coding: UTF-8 -*-

# Description:
# Calculate your body mass with this add-on.

# Thanks:
# Special thanks to the contributors Rui Fonte, Noelia and Dalen
# who have helped make this version possible.

# Author: Edilberto Fonseca
# Email: <edilberto.fonseca@outlook.com>
# Copyright (C) 2022-2025 Edilberto Fonseca
# This file is covered by the GNU General Public License.
# See the file COPYING for more details or visit https://www.gnu.org/licenses/gpl-2.0.html.

# Creation date: 08/11/2022.

import csv
import os
from datetime import datetime

import addonHandler
import gui
import wx
from gui import guiHelper
from logHandler import log

# Get the path of the history file
path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "bmi_history.csv")

# Initializes the translation
addonHandler.initTranslation()


class DialogBMI(wx.Dialog):
	_instance = None

	def __new__(cls, *args, **kwargs):
		if not cls._instance:
			cls._instance = super(DialogBMI, cls).__new__(cls, *args, **kwargs)
		return cls._instance

	def __init__(self, parent, title):
		if hasattr(self, "initialized"):
			return
		self.initialized = True

		# Dialog title.
		self.title = title

		WIDTH = 450
		HEIGHT = 180

		super(DialogBMI, self).__init__(
			parent, title=title, size=(WIDTH, HEIGHT))
		panel = wx.Panel(self)
		boxSizer = wx.BoxSizer(wx.VERTICAL)
		fieldHelper = guiHelper.BoxSizerHelper(panel, wx.VERTICAL)
		buttonSizer = guiHelper.BoxSizerHelper(panel, wx.HORIZONTAL)

		# Create a spinCtrl control
		self.spinHeight = fieldHelper.addLabeledControl(

			# Translators: spin height label.
			_("Enter or select your height in centimeters: "),
			wx.SpinCtrl
		)

		# Defines the initial value for spinHeight.
		self.spinHeight.SetRange(1, 250)

		# Create a spinCtrl control
		self.spinWeight = fieldHelper.addLabeledControl(

			# Translators: Spin Weight label.
			_("Enter or select your weight in kilograms: "),
			wx.SpinCtrl
		)

		# Defines the initial value for spinWeight.
		self.spinWeight.SetRange(1, 500)

		self.buttonCalc = buttonSizer.addItem(
			wx.Button(panel, -1, label=_("C&alculate"))
		)
		self.Bind(wx.EVT_BUTTON, self.onCalc, self.buttonCalc)

		self.buttonClean = buttonSizer.addItem(
			wx.Button(panel, -1, label=_("C&lean"))
		)
		self.Bind(wx.EVT_BUTTON, self.onClean, self.buttonClean)

		self.buttonHistory = buttonSizer.addItem(
			wx.Button(panel, -1, label=_("&History"))
		)
		self.Bind(wx.EVT_BUTTON, self.onShowHistory, self.buttonHistory)

		self.buttonCancel = buttonSizer.addItem(
			wx.Button(panel, wx.ID_CANCEL, label=_("&Cancel"))
		)
		self.Bind(wx.EVT_BUTTON, self.onCancel, id=wx.ID_CANCEL)

		# Define the main layout of the window
		boxSizer.Add(fieldHelper.sizer, border=10, flag=wx.ALL)
		boxSizer.Add(buttonSizer.sizer, border=5, flag=wx.CENTER)
		panel.SetSizerAndFit(boxSizer)

	# Calculate BMI button event.
	def onCalc(self, event):
		try:
			height = self.spinHeight.GetValue()
			weight = self.spinWeight.GetValue()

			if height <= 0 or weight <= 0:
				raise ValueError(_("Height and weight must be greater than zero."))

			calc = float(weight) / ((float(height) / 100)**2)
			calcFormat = "{:.1f}".format(calc)

		except ValueError as e:
			gui.messageBox("{}".format(e), _("Attention"), wx.ICON_ERROR)
			self.spinHeight.SetFocus()
			return

		# Ideal weight range for the given height
		min_weight = round(18.5 * ((height / 100) ** 2), 1)
		max_weight = round(24.9 * ((height / 100) ** 2), 1)
		ideal_weight_text = _("Ideal weight range for your height: {} kg to {} kg.").format(min_weight, max_weight)

		observation_message = _(
			"""
Observation:

For an accurate interpretation of BMI, it is important to consider other factors such as body composition, fat distribution, age, gender, and the individual's overall health.
It is always recommended to consult a healthcare professional, such as a doctor or nutritionist, for a more precise assessment and proper guidance on health and weight."""
		)

		if calc < 18.5:
			msg = _(
				"""Your BMI is {}.

Your BMI indicates that you are underweight.

It's important to consult a doctor or nutritionist
to evaluate your health and identify ways to gain weight in a healthy way.

{}

{}"""
			).format(calcFormat, observation_message, ideal_weight_text)
		elif 18.5 <= calc < 25:
			msg = _(
				"""Your BMI is {}.

Your BMI indicates that you are at a healthy weight.

Keep it up by maintaining a balanced diet and regularly engaging in physical activity.

{}

{}"""
			).format(calcFormat, observation_message, ideal_weight_text)
		elif 25 <= calc < 30:
			msg = _(
				"""Your BMI is {}.

Your BMI indicates that you are overweight.

It's important to consult a doctor or nutritionist
to evaluate your health and identify ways to lose weight in a healthy way.

{}

{}"""
			).format(calcFormat, observation_message, ideal_weight_text)
		elif 30 <= calc < 40:
			msg = _(
				"""Your BMI is {}.

Your BMI indicates that you are overweight.

It's important to consult a doctor or nutritionist
to evaluate your health and identify ways to lose weight in a healthy way.

{}

{}"""
			).format(calcFormat, observation_message, ideal_weight_text)
		else:
			msg = _(
				"""Your BMI is {}.

Your BMI indicates that you are obese.

It's important to consult a doctor or nutritionist
to evaluate your health and identify ways to lose weight in a healthy way and reduce health risks.

{}

{}"""
			).format(calcFormat, observation_message, ideal_weight_text)

		def saveHistory():
			"""
			Appends a new entry to the BMI history log file.
			This function writes the current date and time, height, weight, and calculated BMI format
			to a CSV file specified by the variable `path`. If the file does not exist, it will be created.
			Any exceptions encountered during the file operation are logged as errors.
			Raises:
				Exception: If there is an error while opening or writing to the file.
			"""

			try:
				with open(path, "a", newline='', encoding='utf-8') as f:
					writer = csv.writer(f)
					writer.writerow([datetime.now().isoformat(), height, weight, calcFormat])
			except Exception as e:
				log.error("Error while saving history: {}".format(e))

		saveHistory()

		# Translators: Notification message informing the user of the BMI calculation result.
		gui.messageBox(msg, _("Attention"), wx.ICON_INFORMATION)
		self.onClean(event)

	def onClean(self, event):
		"""
		Event handler that resets the height and weight spin controls to 1 and sets focus to the height control.
		Args:
			event: The event object triggering the handler.
		"""

		self.spinHeight.SetValue(1)
		self.spinWeight.SetValue(1)
		self.spinHeight.SetFocus()

	def onCancel(self, event):
		"""
		Handles the cancel event by destroying the current window.
		Args:
			event: The event object that triggered the cancel action.
		"""

		self.Destroy()

	def onShowHistory(self, event):
		"""
		Handles the event to display the last 10 BMI calculation records from the history file.
		If the history file does not exist, shows a message indicating no history is found.
		If the history file is empty, shows a message indicating the history is empty.
		Otherwise, reads the last 10 entries from the history file, formats them, and displays them in a message box.
		Handles and displays any errors that occur during file reading.
		Args:
			event: The event object triggering this handler.
		"""

		if not os.path.exists(path):
			gui.messageBox(_("No history found."), _("History"), wx.ICON_INFORMATION)
			return

		try:
			with open(path, "r", encoding='utf-8') as f:
				lines = f.readlines()[-10:]  # Mostra os 10 últimos registros
				if not lines:
					gui.messageBox(_("History is empty."), _("History"), wx.ICON_INFORMATION)
					return

				result = _("Last 10 BMI calculations:\n\n")
				for line in lines:
					parts = line.strip().split(",")
					if len(parts) == 4:
						dt, h, w, bmi = parts
						result += _("Date: {} | Height: {} cm | Weight: {} kg | BMI: {}\n").format(dt, h, w, bmi)

				gui.messageBox(result, _("History"), wx.ICON_INFORMATION)
		except Exception as e:
			gui.messageBox(_("Error reading history: {}").format(e), _("History"), wx.ICON_ERROR)
