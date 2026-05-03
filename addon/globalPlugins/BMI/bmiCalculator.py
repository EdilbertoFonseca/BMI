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

import addonHandler

# Initialize translation support
addonHandler.initTranslation()


def validateInputs(height: float, weight: float) -> str | None:
	"""Validates height and weight values.

	Args:
		height (float): The user's height in meters.
		weight (float): The user's weight in kilograms.

	Returns:
		str | None: An error message if the values are invalid, or None if valid.
	"""
	if height <= 0 or weight <= 0:
		return _("Height and weight must be greater than zero.")
	return None


def calculate(height: float, weight: float | None) -> float | None:
	"""Calculates the Body Mass Index (BMI).

	Args:
		height (float): The user's height in meters.
		weight (float | None): The user's weight in kilograms.

	Returns:
		float | None: The calculated BMI value, or None if weight is None.
	"""
	if weight is None:
		return None
	return weight / (height**2)
