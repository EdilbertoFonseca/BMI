# -*- coding: UTF-8 -*-

"""
Author: Edilberto Fonseca <edilberto.fonseca@outlook.com>
Copyright: (C) 2025 Edilberto Fonseca

This file is covered by the GNU General Public License.
See the file COPYING for more details or visit:
https://www.gnu.org/licenses/gpl-2.0.html

Created on:11/ 08/2022
"""

import addonHandler
from typing import Optional

# Initialize translation support
addonHandler.initTranslation()


def validate_inputs(height_m: float, weight_kg: float) -> Optional[str]:
	"""
	Validate height and weight values before BMI calculation.

	Parameters
	----------
	height_m : float
		Height in meters. Must be greater than zero.
	weight_kg : float
		Weight in kilograms. Must be greater than zero.

	Returns
	-------
	Optional[str]
		A translated error message if validation fails, otherwise None.

	Notes
	-----
	This function performs simple validation. Additional rules (e.g.,
	maximum safe limits) can be added if needed.
	"""

	if height_m <= 0 or weight_kg <= 0:
		return _("Height and weight must be greater than zero.")

	return None


def calculate_bmi(height_m: float, weight_kg: float) -> float:
	"""
	Calculate Body Mass Index (BMI).

	Parameters
	----------
	height_m : float
		Height in meters. Must be greater than zero.
	weight_kg : float
		Weight in kilograms.

	Returns
	-------
	float
		The BMI value.

	Raises
	------
	ValueError
		If height_m is zero or negative.

	Notes
	-----
	BMI is defined as: weight (kg) / height (m)^2
	"""

	if height_m <= 0:
		raise ValueError("Height must be greater than zero for BMI calculation.")

	return weight_kg / (height_m ** 2)
