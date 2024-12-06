"""
Argilla Dataset Manager - A tool for managing and uploading datasets to Argilla.
"""

from argilla_dataset_manager.utils.dataset_manager import DatasetManager
from argilla_dataset_manager.utils.argilla_client import get_argilla_client
from argilla_dataset_manager.datasets.settings_manager import SettingsManager

__version__ = "0.1.0"
__all__ = ["DatasetManager", "get_argilla_client", "SettingsManager"] 