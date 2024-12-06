from ..en_q_client import poll
from .base import Command


class PollCommand(Command):
    """Command used to retrive training data in
    SDK queue on server"""

    def run(self):
        data = poll()
        # send to output stream
        print(data)
