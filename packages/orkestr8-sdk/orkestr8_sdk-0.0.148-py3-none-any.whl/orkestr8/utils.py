import os
from pathlib import Path

from .settings import DATA_OUTPUT_FILE_LOCATION, PID_FILE_LOCATION


def get_pid_save_location() -> Path:
    os.makedirs(str(PID_FILE_LOCATION.parent), exist_ok=True)
    if not Path(PID_FILE_LOCATION).exists():
        with open(str(PID_FILE_LOCATION), "w"):
            pass
    return PID_FILE_LOCATION


def get_data_output_file() -> Path:
    os.makedirs(str(DATA_OUTPUT_FILE_LOCATION.parent), exist_ok=True)
    if not Path(DATA_OUTPUT_FILE_LOCATION).exists():
        with open(str(DATA_OUTPUT_FILE_LOCATION), "w"):
            pass
    return DATA_OUTPUT_FILE_LOCATION
