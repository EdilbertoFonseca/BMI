# -*- coding: UTF-8 -*-

"""
Handles saving and loading BMI calculation history in JSON format.
"""

import json
import os
from datetime import datetime
from typing import List, Dict, Optional
import addonHandler

from logHandler import log

# Initializes the translation
addonHandler.initTranslation()

# Path to the history file
HISTORY_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "bmi_history.json")


def load_history() -> Optional[List[Dict]]:
	"""Loads the BMI calculation history from the JSON file.

	Returns:
		Optional[List[Dict]]: A list of history entries, or None if the file doesn't exist or is empty.
	"""
	if not os.path.exists(HISTORY_FILE):
		return None

	try:
		with open(HISTORY_FILE, "r", encoding="utf-8") as file:
			data = json.load(file)
			if not data:
				return None
			return data
	except Exception as e:
		log.error("Failed to load BMI history: %s", e)
		return None


def save_to_history(height: int, weight: int, bmi: float) -> None:
	"""Saves a new BMI entry to the history file.

	Args:
		height (int): The height in centimeters.
		weight (int): The weight in kilograms.
		bmi (float): The calculated BMI value.
	"""
	entry = {
		"timestamp": datetime.now().isoformat(),
		"height": height,
		"weight": weight,
		"bmi": "{:.1f}".format(bmi)
	}

	try:
		history = load_history() or []
		history.append(entry)

		with open(HISTORY_FILE, "w", encoding="utf-8") as file:
			json.dump(history, file, indent=2, ensure_ascii=False)

	except Exception as e:
		log.error("Failed to save BMI entry: %s", e)
