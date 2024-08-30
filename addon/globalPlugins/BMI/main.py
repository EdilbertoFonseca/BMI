# -*- coding: UTF-8 -*-

# Description: Calculate your body mass with this add-on.
# Auth	or: Edilberto Fonseca.
# Email: edilberto.fonseca@outlook.com.
# Thanks: Special thanks to the contributors Rui Fonte, Noelia e Dalen who have helped make this version
# possible.
# Date of creation: 08/11/2022.

# import the necessary modules.
import addonHandler
import queueHandler
import ui
import wx
from gui import guiHelper
from gui import messageBox

# Module required to carry out the translations.
addonHandler.initTranslation()

# Get the title of the addon defined in the summary.
ADDON_SUMMARY = addonHandler.getCodeAddon().manifest["summary"]


class DialogBMI(wx.Dialog):
	_instance = None

	def __new__(cls, *args, **kwargs):
		if not cls._instance:
			cls._instance = super(DialogBMI, cls).__new__(cls, *args, **kwargs)
		else:
			msg = _("An instance of {} is already open.").format(ADDON_SUMMARY)
			queueHandler.queueFunction(queueHandler.eventQueue, ui.message, msg)
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

		# Create a spinCtrl control for height.
		self.spinHeight = fieldHelper.addLabeledControl(
			# Translators: spin height label.
			_("Enter or select your height in centimeters: "),
			wx.SpinCtrl
		)
		self.spinHeight.SetRange(0, 250)

		# Create a spinCtrl control for weight.
		self.spinWeight = fieldHelper.addLabeledControl(
			# Translators: Spin Weight label.
			_("Enter or select your weight in kilograms: "),
			wx.SpinCtrl
		)
		self.spinWeight.SetRange(0, 500)

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

	def onCalc(self, event):
		"""
		Calculates Body Mass Index (BMI) based on the given height and weight and displays the result.

		Args:
			event (wx.Event): The event triggered by the BMI calculation button.

		Raises:
			ValueError: If the given height or weight is less than or equal to 0.
		"""

		try:
			height = self.spinHeight.GetValue()
			weight = self.spinWeight.GetValue()

			# Validate if height and weight are greater than 0.
			if height <= 0 or weight <= 0:
				raise ValueError(_("Height and weight must be greater than 0."))

			calc = float(weight) / ((float(height) / 100) ** 2)
			calcFormat = f"{calc:.1f}"

		except ValueError as e:
			self.show_message(f"{e}", _("Attention"), wx.ICON_ERROR)
			self.spinHeight.SetFocus()
			return

		msg = self.getBmiMessage(calc, calcFormat)
		self.show_message(msg, _("Attention"))
		self.onClean(event)

	def getBmiMessage(self, calc, calcFormat):
		"""
		Generates an informative message based on the calculated Body Mass Index (BMI).

		Args:
calc (float): The calculated BMI value.
		calcFormat (str): The BMI value formatted as a string with one decimal place.
	Returns:
		str: A message that provides BMI interpretation and recommendations based on the calculated value.
		"""

		observation_message = _(
			"""Observation:
For a proper interpretation of BMI, it is recommended to consider other factors such as body composition, fat distribution, age, gender, and overall health.

It is always recommended to consult a healthcare professional, such as a physician or nutritionist, for a more accurate assessment and proper guidance on health and weight."""
		)

		if calc < 18.5:
			msg = _(
				"""Your BMI is {}.

Your BMI indicates that you are underweight.

It's important to consult a doctor or a nutritionist to evaluate your health and identify ways to gain weight in a healthy way.

{}""").format(calcFormat, observation_message)
		elif 18.5 <= calc < 25:
			msg = _(
				"""Your BMI is {}.

Your BMI indicates that you are at a healthy weight.

Keep it up by maintaining a balanced diet and regularly engaging in physical activity.

{}""").format(calcFormat, observation_message)
		elif 25 <= calc < 30:
			msg = _(
				"""Your BMI is {}.

Your BMI indicates that you are overweight.

It's important to consult a doctor or a nutritionist to evaluate your health and identify ways to lose weight healthily.

{}""").format(calcFormat, observation_message)
		elif 30 <= calc < 40:
			msg = _(
				"""Your BMI is {}.

Your BMI indicates that you are obese (Class I or II).

It's important to consult a doctor or nutritionist to evaluate your health and identify ways to lose weight in a healthy way.

{}""").format(calcFormat, observation_message)
		else:
			msg = _(
				"""Your BMI is {}.

Your BMI indicates that you are severely obese (Class III).

It's crucial to consult a doctor or a nutritionist to evaluate your health and to identify ways to reduce health risks.

{}""").format(calcFormat, observation_message)

		return msg

	def onClean(self, event):
		"""
		Clear button action.

		Args:
			event (wx.Event): The event triggered by the clear button.
		"""
		self.spinHeight.SetValue(0)
		self.spinWeight.SetValue(0)
		self.spinHeight.SetFocus()

	def show_message(self, message, caption=_("Attention"), style=wx.OK | wx.ICON_INFORMATION):
		"""
		Formats and displays messages to the user.

		Args:
			message (str): Message to be displayed.
			caption (str, optional): Window title. The default is _("Message").
			style (int, optional): Message box style, combining flags like wx.OK, wx.CANCEL, wx.ICON_INFORMATION, etc.
			The default is wx.OK | wx.ICON_INFORMATION.
		"""
		messageBox(message, caption, style)

	def onCancel(self, event):
		"""
		Ends the dialogue, destroying the window.

		Args:
			event (wx.Event): The event triggered by the cancel button.
		"""
		self.Destroy()
