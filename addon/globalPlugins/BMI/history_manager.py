# -*- coding: UTF-8 -*-

"""
Author: Edilberto Fonseca <edilberto.fonseca@outlook.com>
Copyright: (C) 2025 Edilberto Fonseca

This file is covered by the GNU General Public License.
See the file COPYING for more details or visit:
https://www.gnu.org/licenses/gpl-2.0.html

Created on: 11/08/2022
"""

import json
import os
from datetime import datetime
from typing import Dict, List

import addonHandler
from logHandler import log

# Initialize translation support
addonHandler.initTranslation()

# Get the addon object
addon = addonHandler.getCodeAddon()

# Build the correct data directory path for the addon
DATA_DIR = os.path.join(addon.path, "data")

# Create the directory if missing
os.makedirs(DATA_DIR, exist_ok=True)

# Full path to the history file
HISTORY_FILE = os.path.join(DATA_DIR, "bmi_history.json")

def load_history() -> List[Dict]:
	"""
	Load BMI calculation history from disk.

	Returns
	-------
	List[Dict]
		A list of stored history entries. Returns an empty list if the
		file does not exist, is empty, or contains invalid data.

	Notes
	-----
	This function never returns None. Returning a consistent list
	prevents unnecessary checks in the caller.
	"""

	if not os.path.exists(HISTORY_FILE):
		return []

	try:
		with open(HISTORY_FILE, "r", encoding="utf-8") as file:
			data = json.load(file)
			if isinstance(data, list):
				return data
			else:
				log.error("BMI history file contains invalid structure.")
				return []
	except Exception as e:
		log.error(f"Failed to load BMI history: {e}")
		return []


def save_to_history(height_cm: int, weight_kg: int, bmi_value: float) -> None:
	"""
	Save a new BMI calculation entry to persistent storage.

	Parameters
	----------
	height_cm : int
		User height in centimeters.
	weight_kg : int
		User weight in kilograms.
	bmi_value : float
		Calculated BMI value.

	Notes
	-----
	The history is stored in JSON format as a list of dictionaries.
	Each entry includes a timestamp in ISO format.
	"""

	entry = {
		"timestamp": datetime.now().isoformat(),
		"height": height_cm,
		"weight": weight_kg,
		"bmi": round(bmi_value, 1)  # Save as numeric value, not string
	}

	try:
		history = load_history()
		history.append(entry)

		with open(HISTORY_FILE, "w", encoding="utf-8") as file:
			json.dump(history, file, indent=2, ensure_ascii=False)

	except Exception as e:
		log.error(f"Failed to save BMI entry: {e}")
