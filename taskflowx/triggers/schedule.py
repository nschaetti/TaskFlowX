#  ████████╗ █████╗ ███████╗██╗  ███████╗██╗      ██████╗ ██╗  ██╗
#  ╚══██╔══╝██╔══██╗██╔════╝██║  ██╔════╝██║     ██╔═══██╗██║  ██║
#     ██║   ███████║███████╗██║  █████╗  ██║     ██║   ██║███████║
#     ██║   ██╔══██║╚════██║██║  ██╔══╝  ██║     ██║   ██║██╔══██║
#     ██║   ██║  ██║███████║██║  ██║     ███████╗╚██████╔╝██║  ██║
#     ╚═╝   ╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝     ╚══════╝ ╚═════╝ ╚═╝  ╚═╝
#
#  TaskFlowX - A lightweight and modular workflow automation engine
#
#  This code is licensed under the GNU General Public License (GPL).
#  You are free to modify and distribute it under the terms of the GPL.
#
#  (c) 2025 TaskFlowX Nils Schaetti <n.schaetti@gmail.com>

# Imports
import time
import threading
from .base import Trigger


# Schedule trigger
class ScheduleTrigger(Trigger):
    """
    Schedule trigger.
    """

    # Constructor
    def __init__(
            self,
            interval: int
    ):
        """
        Constructor.

        Args:
        - interval: The interval to trigger the callback.
        """
        self.params = {
            "interval": interval
        }
    # end __init__

    # Pull the trigger
    def start(self, callback):
        """
        Start the schedule trigger.

        Args:
        - callback: The callback function to call.
        """
        def run():
            while True:
                callback()
                time.sleep(self.params["interval"])
            # end while
        # end run

        # Start the thread
        threading.Thread(target=run, daemon=True).start()
    # end start

    @staticmethod
    def trigger_name():
        """
        Get the trigger name.
        """
        return "schedule"
    # end trigger_name

# end ScheduleTrigger

