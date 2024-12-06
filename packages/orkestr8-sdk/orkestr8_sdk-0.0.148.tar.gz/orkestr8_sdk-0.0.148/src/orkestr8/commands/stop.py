import logging
import os
import signal
import time
from dataclasses import dataclass
from typing import Union

from orkestr8.utils import get_pid_save_location

from .base import Command

LOGGER = logging.getLogger()


@dataclass
class StopArgs:
    pid: Union[str, None]


class StopCommand(Command[StopArgs]):
    @staticmethod
    def parse(args) -> StopArgs:
        return StopArgs(args.pid)

    def run(self):
        LOGGER.info("Shutdown command invoked")
        with open(get_pid_save_location()) as f:
            pid = f.read().split(":")[-1].strip()

        os.kill(pid, signal.SIGTERM)
        for _ in range(10):  # Check up to 10 times
            if not os.path.exists(f"/proc/{pid}"):
                print(f"Process {pid} has terminated.")
                break
            time.sleep(1)
        LOGGER.info("Shutdown completed successfully")
