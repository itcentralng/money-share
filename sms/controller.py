import os
import africastalking
import re
from dotenv import load_dotenv

load_dotenv()


username = os.environ.get("AFRICASTALKING_USER")
api_key = os.environ.get("AFRICASTALKING_KEY")
africastalking.initialize(username, api_key)


class SMS:
    patterns = {
        "send": r"^send \d+ \+\d{13}$",
        "help": r"^help(?: (info|send|create))?$",
        "info": r"^info$",
        "create": r"^create$",
    }

    def __init__(self):
        self.sms = africastalking.SMS

    def send(self, recipients: list[str], message: str):
        try:
            response = self.sms.send(
                message, recipients, os.environ.get("AFRICASTALKING_NUMBER")
            )
            print(response)
        except Exception as e:
            print(f"Houston, we have a problem: {e}")

    def check_structure(self, input_string: str):
        # Split the input string to get the command
        command = input_string.split()[0]

        if command in self.patterns:
            if re.match(self.patterns[command], input_string):
                return [True, f"'{input_string}' matches the expected structure."]
            else:
                return [
                    False,
                    f"'{input_string}' does not match the expected structure.",
                ]
        else:
            return [False, f"Unknown command '{command}'."]
