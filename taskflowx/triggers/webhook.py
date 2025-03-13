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
from flask import Flask, request
from .base import Trigger
import threading


# Webhook trigger
class WebhookTrigger(Trigger):
    """
    Webhook trigger.
    """

    def __init__(
            self,
            path
    ):
        """
        Constructor

        Args:
        - path: The path to listen to.
        """
        self.params = {
            "path": path
        }
    # end __init__

    def start(
            self,
            callback
    ):
        """
        Start

        Args:
        - callback: The callback function to call.
        """
        # Flask app
        app = Flask(__name__)

        # Handle webhook
        @app.route(self.params["path"], methods=["POST"])
        def handle_webhook():
            callback(request.json)
            return {"status": "ok"}
        # end handle_webhook

        # Start a thread
        threading.Thread(target=app.run, kwargs={"port": 5000}).start()
    # end start

    # Trigger name
    @staticmethod
    def trigger_name():
        """
        Get the trigger name.
        """
        return "webhook"
    # end trigger_name

# end WebhookTrigger
