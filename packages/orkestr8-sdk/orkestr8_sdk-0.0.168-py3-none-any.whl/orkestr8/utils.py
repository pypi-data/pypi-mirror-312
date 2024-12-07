import os
from pathlib import Path

from .settings import DATA_OUTPUT_FILE_LOCATION, PID_FILE_LOCATION


def get_pid_save_location() -> Path:
    if not Path(PID_FILE_LOCATION).exists():
        os.makedirs(str(PID_FILE_LOCATION.parent), exist_ok=True)
        with open(str(PID_FILE_LOCATION), "w"):
            pass
    return PID_FILE_LOCATION


def get_data_output_file() -> Path:
    if not Path(DATA_OUTPUT_FILE_LOCATION).exists():
        os.makedirs(str(DATA_OUTPUT_FILE_LOCATION.parent), exist_ok=True)
        with open(str(DATA_OUTPUT_FILE_LOCATION), "w"):
            pass
    return DATA_OUTPUT_FILE_LOCATION
