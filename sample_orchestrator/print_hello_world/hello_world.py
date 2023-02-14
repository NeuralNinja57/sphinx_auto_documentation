"""
Test code for testing sphinx utility
"""

import pandas as pd


class HelloWorld:
    def __init__(self):
        self.name = "Shubham"

    def say_hello(self, msg):
        """
        Function to give out a message

        Args:
            msg (str): Message

        Returns:
            str: Greet the user and deliver the message
        """
        return f"Hello {self.name}, {msg}"

    def say_hello_again(self, msg):
        """
        Function to give out a message again

        Parameters:
            msg (str): Message

        Returns:
            str: Greet the user and deliver the message
        """
        return f"Hello Again {self.name}, {msg}"
