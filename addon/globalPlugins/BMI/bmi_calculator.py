# -*- coding: UTF-8 -*-

"""
BMI calculator logic and message handler.

This module provides functions to calculate the Body Mass Index (BMI)
and return appropriate messages based on the user's gender and BMI value.
"""

import addonHandler
from typing import Optional

# Initializes the translation
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
