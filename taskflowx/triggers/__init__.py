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
from .base import Trigger
from .email import EmailTrigger
from .schedule import ScheduleTrigger
from .webhook import WebhookTrigger

# Export
__all__ = ["Trigger", "EmailTrigger", "ScheduleTrigger", "WebhookTrigger"]
