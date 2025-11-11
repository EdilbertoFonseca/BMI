# -*- coding: UTF-8 -*-

"""
Description: BMI calculator logic and message handler.

This module provides functions to calculate the Body Mass Index (BMI)
and return appropriate messages based on the user's gender and BMI value.
"""

# Author: Edilberto Fonseca
# Email: <edilberto.fonseca@outlook.com>
# Copyright (C) 2025 Edilberto Fonseca
# This file is covered by the GNU General Public License.
# See the file COPYING for more details or visit https://www.gnu.org/licenses/gpl-2.0.html.

# Date of creation 11/08/2022.

from typing import Optional

import addonHandler

# Initialize translation support
addonHandler.initTranslation()

def validate_inputs(height: float, weight: float) -> Optional[str]:
	"""Validates height and weight values.

	Args:
		height (float): The user's height in meters.
		weight (float): The user's weight in kilograms.

	Returns:
		Optional[str]: An error message if the values are invalid, or None if valid.
	"""
	if height <= 0 or weight <= 0:
		return _("Height and weight must be greater than zero.")
	return None


def calculate_bmi(height: float, weight: float) -> float:
	"""Calculates the Body Mass Index (BMI).

	Args:
		height (float): The user's height in meters.
		weight (float): The user's weight in kilograms.

	Returns:
		float: The calculated BMI value.
	"""
	return weight / (height ** 2)
