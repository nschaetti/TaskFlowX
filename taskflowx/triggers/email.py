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
import imaplib
import email
from imapclient import IMAPClient
from .base import Trigger
from taskflowx import logger


class EmailTrigger(Trigger):
    """
    Trigger to check emails and call a workflow with the email data.
    """

    def __init__(
            self,
            imap_server: str,
            username: str,
            password: str,
            mailbox: str = "INBOX",
            interval: int = 60
    ):
        """
        Constructor.

        Args:
        - imap_server: The IMAP server.
        - username: The username.
        - password: The password.
        - mailbox: The mailbox to check.
        - interval: The interval to check for new emails.
        """
        super().__init__()
        self.imap_server = imap_server
        self.username = username
        self.password = password
        self.mailbox = mailbox
        self.interval = interval
    # end __init__

    # Check email
    def check_email(
            self,
            callback
    ):
        """
        Check email and call the callback function with the email data.

        Args:
        - callback: The callback function to call with the email data.
        """
        try:
            with IMAPClient(self.imap_server) as client:
                # Login and select mailbox
                client.login(self.username, self.password)
                client.select_folder(self.mailbox)

                # Search for unseen messages
                messages = client.search("UNSEEN")
                for msgid in messages:
                    raw_msg = client.fetch(msgid, ["RFC822"])[msgid][b"RFC822"]
                    msg = email.message_from_bytes(raw_msg)

                    # Call the workflow with the email data
                    callback({
                        "from": msg["From"],
                        "subject": msg["Subject"],
                        "body": self.get_email_body(msg),
                    })

                    #
                    client.add_flags(msgid, [imaplib.SEEN])
                # end for
            # end with
        except Exception as e:
            logger.error(f"Erreur EmailTrigger: {e}")
        # end try
    # end check_email

    # Get email body
    def get_email_body(self, msg):
        """
        Extract the email body from the message.

        Args:
        - msg: The email message.
        """
        if msg.is_multipart():
            for part in msg.walk():
                if part.get_content_type() == "text/plain":
                    return part.get_payload(decode=True).decode()
                # end if
            # end for
        else:
            return msg.get_payload(decode=True).decode()
        return ""
    # end get_email_body

    # Start
    def start(self, callback):
        """
        Start the email trigger.

        Args:
        - callback: The callback function to call.
        """
        def run():
            while True:
                self.check_email(callback)
                time.sleep(self.interval)
            # end while
        # end run

        # Start the thread
        threading.Thread(target=run, daemon=True).start()
    # end start

    # Trigger name
    @staticmethod
    def trigger_name():
        """
        Trigger name
        """
        return "email"
    # end trigger_name

# end EmailTrigger

