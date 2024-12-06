import os
import re
from pathlib import Path
from typing import TypedDict, cast

from .settings import DATA_OUTPUT_FILE_LOCATION, PID_FILE_LOCATION


class TrainingData(TypedDict):
    epoch: int
    train_acc: str
    test_acc: str
    time: str
    train_loss: float
    val_loss: float
    dir_name: str


def build_training_data_response(text: str) -> TrainingData:
    result = {}
    for rk, annotate in TrainingData.__annotations__.items():
        data = re.search(rf"{rk}=([\"a-z\d\._\'%]+)\s*,?", text, flags=re.I)
        if data:
            result[rk] = annotate(data.group(1))
        else:
            raise Exception(f"All args must be defined. Missing in training data {rk}")
    return cast(TrainingData, result)


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
