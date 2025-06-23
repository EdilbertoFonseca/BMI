# -*- coding: UTF-8 -*-

# Description: Calculate your body mass with this add-on.

# Special thanks to the contributors Rui Fonte, Noelia, and Dalen, whose help made this project possible.

# Author: Edilberto Fonseca
# Email: <edilberto.fonseca@outlook.com>
# Copyright (C) 2022-2025 Edilberto Fonseca
# This file is covered by the GNU General Public License.
# See the file COPYING for more details or visit https://www.gnu.org/licenses/gpl-2.0.html.

# Creation date: 08/11/2022.

import json
import os
from datetime import datetime

import addonHandler
import gui
import wx
from gui import guiHelper
from logHandler import log

# Get the path of the history file
path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "bmi_history.json")

# Initialize translation
addonHandler.initTranslation()


class BMIDialog(wx.Dialog):
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
            _("Enter or select your height in centimeters: "), wx.SpinCtrl
        )
        self.heightCtrl.SetRange(1, 250)

        self.weightCtrl = fieldHelper.addLabeledControl(
            _("Enter or select your weight in kilograms: "), wx.SpinCtrl
        )
        self.weightCtrl.SetRange(1, 500)

        self.calcButton = buttonHelper.addItem(
            wx.Button(panel, -1, label=_("C&alculate"))
        )
        self.Bind(wx.EVT_BUTTON, self.onCalculate, self.calcButton)

        self.clearButton = buttonHelper.addItem(
            wx.Button(panel, -1, label=_("C&lear"))
        )
        self.Bind(wx.EVT_BUTTON, self.onClear, self.clearButton)

        self.historyButton = buttonHelper.addItem(
            wx.Button(panel, -1, label=_("&History"))
        )
        self.Bind(wx.EVT_BUTTON, self.onShowHistory, self.historyButton)

        self.cancelButton = buttonHelper.addItem(
            wx.Button(panel, wx.ID_CANCEL, label=_("&Cancel"))
        )
        self.Bind(wx.EVT_BUTTON, self.onCancel, id=wx.ID_CANCEL)

        mainSizer.Add(fieldHelper.sizer, border=10, flag=wx.ALL)
        mainSizer.Add(buttonHelper.sizer, border=5, flag=wx.CENTER)
        panel.SetSizerAndFit(mainSizer)

    def onCalculate(self, event):
        try:
            height = self.heightCtrl.GetValue()
            weight = self.weightCtrl.GetValue()

            if height <= 0 or weight <= 0:
                raise ValueError(_("Height and weight must be greater than zero."))

            bmi = float(weight) / ((float(height) / 100) ** 2)
            bmiFormatted = "{:.1f}".format(bmi)

        except ValueError as e:
            gui.messageBox(str(e), _("Attention"), wx.ICON_ERROR)
            self.heightCtrl.SetFocus()
            return

        min_weight = round(18.5 * ((height / 100) ** 2), 1)
        max_weight = round(24.9 * ((height / 100) ** 2), 1)
        ideal_range = _("Ideal weight range for your height: {} kg to {} kg.").format(min_weight, max_weight)

        observation = _(
            """Observation:

For an accurate interpretation of BMI, it is important to consider other factors such as body composition, fat distribution, age, gender, and overall health.
It is always recommended to consult a healthcare professional for proper guidance on health and weight."""
        )

        if bmi < 18.5:
            msg = _("""Your BMI is {}.

You are underweight.

It is important to consult a doctor or nutritionist to identify healthy ways to gain weight.

{}

{}""").format(bmiFormatted, observation, ideal_range)
        elif 18.5 <= bmi < 25:
            msg = _("""Your BMI is {}.

You are at a healthy weight.

Maintain it with a balanced diet and regular physical activity.

{}

{}""").format(bmiFormatted, observation, ideal_range)
        elif 25 <= bmi < 30:
            msg = _("""Your BMI is {}.

You are overweight.

It is important to consult a doctor or nutritionist to identify healthy weight loss strategies.

{}

{}""").format(bmiFormatted, observation, ideal_range)
        elif 30 <= bmi < 40:
            msg = _("""Your BMI is {}.

You are significantly overweight.

Please consult a healthcare provider for guidance.

{}

{}""").format(bmiFormatted, observation, ideal_range)
        else:
            msg = _("""Your BMI is {}.

Your BMI indicates that you are in the obese range.

It is important to consult a doctor to reduce health risks through safe weight loss.

{}

{}""").format(bmiFormatted, observation, ideal_range)

        def saveHistory():
            entry = {
                "timestamp": datetime.now().isoformat(),
                "height": height,
                "weight": weight,
                "bmi": bmiFormatted
            }

            try:
                history = []
                if os.path.exists(path):
                    with open(path, "r", encoding="utf-8") as f:
                        history = json.load(f)

                history.append(entry)

                with open(path, "w", encoding="utf-8") as f:
                    json.dump(history, f, indent=2, ensure_ascii=False)

            except Exception as e:
                log.error("Error while saving history: {}".format(e))

        saveHistory()
        gui.messageBox(msg, _("Attention"), wx.ICON_INFORMATION)
        self.onClear(event)

    def onClear(self, event):
        self.heightCtrl.SetValue(1)
        self.weightCtrl.SetValue(1)
        self.heightCtrl.SetFocus()

    def onCancel(self, event):
        self.Destroy()

    def onShowHistory(self, event):
        if not os.path.exists(path):
            gui.messageBox(_("No history found."), _("History"), wx.ICON_INFORMATION)
            return

        try:
            with open(path, "r", encoding="utf-8") as file:
                data = json.load(file)
                if not data:
                    gui.messageBox(_("The history is empty."), _("History"), wx.ICON_INFORMATION)
                    return

                last_entries = data[-10:]
                result = _("Last 10 BMI calculations:\n\n")
                for record in last_entries:
                    dt = datetime.fromisoformat(record["timestamp"])
                    formatted_dt = dt.strftime("%d/%m/%Y %H:%M")
                    result += _("Date: {} | Height: {} cm | Weight: {} kg | BMI: {}\n").format(
                        formatted_dt, record["height"], record["weight"], record["bmi"]
                    )

                gui.messageBox(result, _("History"), wx.ICON_INFORMATION)

        except Exception as error:
            gui.messageBox(_("Error reading history: {}").format(error), _("History"), wx.ICON_ERROR)
