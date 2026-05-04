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

import json
import os
from datetime import datetime

import addonHandler
import globalVars
from logHandler import log

# Initialize translation support
addonHandler.initTranslation()

# Path to the history file
ADDON_DATA_DIR = getattr(globalVars.appArgs, "configPath", "")
HISTORY_PATH = os.path.join(ADDON_DATA_DIR, "BMIHistory.json")

# Type alias for one history entry
HistoryEntry = dict[str, str | int | float]


def loadHistory() -> list[HistoryEntry] | None:
	"""Loads the BMI calculation history from the JSON file.

	Returns:
		A list of history entries, or None if the file doesn't exist or is empty.
	"""
	if not os.path.exists(HISTORY_PATH):
		return None

	try:
		with open(HISTORY_PATH, "r", encoding="utf-8") as file:
			data = json.load(file)

			if not isinstance(data, list) or not data:
				return None

			return data

	except Exception as e:
		log.error("Failed to load BMI history: %s", e)
		return None


def saveToHistory(height: int, weight: int, bmi: float) -> None:
	"""Saves a new BMI entry to the history file.

	Args:
		height: The height in centimeters.
		weight: The weight in kilograms.
		bmi: The calculated BMI value.
	"""
	entry: HistoryEntry = {
		"timestamp": datetime.now().isoformat(),
		"height": height,
		"weight": weight,
		"bmi": round(bmi, 1),
	}

	try:
		history = loadHistory() or []
		history.append(entry)

		with open(HISTORY_PATH, "w", encoding="utf-8") as file:
			json.dump(history, file, indent=2, ensure_ascii=False)

	except Exception as e:
		log.error("Failed to save BMI entry: %s", e)
