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

# Standard NVDA imports.
import addonHandler
import gui
from gui import guiHelper
import wx


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
		HEIGHT = 150

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
			calcFormat = f"{calc:.1f}"

		except ValueError as e:
			gui.messageBox("%s" % e, _("Attention"), wx.ICON_ERROR)
			self.spinHeight.SetFocus()
			return

		observation_message = _(
			"""
Observation:
For a proper interpretation of BMI, it is recommended to consider other factors such as body composition, fat
distribution, age, gender and general health of the person.

It is always recommended to consult a healthcare professional, such as a physician or nutritionist, for a more
accurate assessment and proper guidance on health and weight."""
		)

		if calc < 18.5:
			msg = _(
				"""Your BMI is {}.

Your BMI indicates that you are underweight.

It's important to consult a doctor or nutritionist
to evaluate your health and identify ways to gain weight in a healthy way.

{}"""
			).format(calcFormat, observation_message)
		elif 18.5 <= calc < 25:
			msg = _(
				"""Your BMI is {}.

Your BMI indicates that you are at a healthy weight.

Keep it up by maintaining a balanced diet and regularly engaging in physical activity.

{}"""
			).format(calcFormat, observation_message)
		elif 25 <= calc < 30:
			msg = _(
				"""Your BMI is {}.

Your BMI indicates that you are overweight.

It's important to consult a doctor or nutritionist
to evaluate your health and identify ways to lose weight in a healthy way.

{}"""
			).format(calcFormat, observation_message)
		elif 30 <= calc < 40:
			msg = _(
				"""Your BMI is {}.

Your BMI indicates that you are overweight.

It's important to consult a doctor or nutritionist
to evaluate your health and identify ways to lose weight in a healthy way.

{}"""
			).format(calcFormat, observation_message)
		else:
			msg = _(
				"""Your BMI is {}.

Your BMI indicates that you are obese.

It's important to consult a doctor or nutritionist
to evaluate your health and identify ways to lose weight in a healthy way and reduce health risks.

{}"""
			).format(calcFormat, observation_message)

		# Translators: Notification message informing the user of the BMI calculation result.
		gui.messageBox(msg, _("Attention"), wx.ICON_INFORMATION)
		self.onClean(event)

# Clear button event.
	def onClean(self, event):
		self.spinHeight.SetValue(1)
		self.spinWeight .SetValue(1)
		self.spinHeight.SetFocus()

# Cancel button event.
	def onCancel(self, event):
		self.Destroy()
