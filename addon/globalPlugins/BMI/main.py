# -*- coding: UTF-8 -*-

# Calculate your body mass with this add-on.
# Author: Edilberto Fonseca.
# Thanks: To Rui Fontes, for his collaboration and guidance during the development of the addon.
# Creation date: 08/11/2022.

# Standard NVDA imports.
import addonHandler
import gui
from gui import guiHelper
import wx
import ui

# Module required to carry out the translations.
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
			calc = float(weight) / ((float(height) / 100)**2)

			# Format the value of "calc" with one decimal place and store it in "calcFormat".
			calcFormat = f"{calc:.1f}"

		except ValueError as e:
			# Translators: Mensagem exibida quando ocorre algun erro inesperado.
			gui.messageBox("%s" %e,
						   _("Atention"), wx.ICON_ERROR)
			self.spinHeight.SetFocus()

		if calc < 18.5:
			msg = \
				_("""Your BMI is {}.

Your BMI indicates that you are underweight.

It's important to consult a doctor or nutritionist to evaluate your health and identify ways to gain weight in a healthy way.

Observation:
For a proper interpretation of BMI, it is recommended to consider other factors such as body composition, fat distribution, age, gender and general health of the person.
It is always recommended to consult a healthcare professional, such as a physician or nutritionist, for a more accurate assessment and proper guidance on health and weight.""").format(calcFormat)
		elif 18.5 <= calc < 25:
			msg = \
				_("""Your BMI is {}.

Your BMI indicates that you are at a healthy weight.

Keep it up by maintaining a balanced diet and regularly engaging in physical activity.

Observation:
For a proper interpretation of BMI, it is recommended to consider other factors such as body composition, fat distribution, age, gender and general health of the person.
It is always recommended to consult a healthcare professional, such as a physician or nutritionist, for a more accurate assessment and proper guidance on health and weight.""").format(calcFormat)
		elif 25 <= calc < 30:
			msg = \
				_("""Your BMI is {}.

Your BMI indicates that you are overweight.

It's important to consult a doctor or nutritionist to evaluate your health and identify ways to lose weight in a healthy way.

Observation:
For a proper interpretation of BMI, it is recommended to consider other factors such as body composition, fat distribution, age, gender and general health of the person.
It is always recommended to consult a healthcare professional, such as a physician or nutritionist, for a more accurate assessment and proper guidance on health and weight.""").format(calcFormat)
		elif 30 <= calc < 40:
			msg = \
				_("""Your BMI is {}.

Your BMI indicates that you are overweight.

It's important to consult a doctor or nutritionist to evaluate your health and identify ways to lose weight in a healthy way.

Observation:
For a proper interpretation of BMI, it is recommended to consider other factors such as body composition, fat distribution, age, gender and general health of the person.
It is always recommended to consult a healthcare professional, such as a physician or nutritionist, for a more accurate assessment and proper guidance on health and weight.""").format(calcFormat)
		else:
			msg = \
				_("""Your BMI is {}.

Your BMI indicates that you are obese.

It's important to consult a doctor or nutritionist to evaluate your health and identify ways to lose weight in a healthy way and reduce health risks.

Observation:
For a proper interpretation of BMI, it is recommended to consider other factors such as body composition, fat distribution, age, gender and general health of the person.
It is always recommended to consult a healthcare professional, such as a physician or nutritionist, for a more accurate assessment and proper guidance on health and weight.""").format(calcFormat)

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
