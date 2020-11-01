"""Contains different types of loggers
"""
from abc import ABC


class Logger(ABC):
    """The abstract base class for Logger

    """

    @staticmethod
    def type() -> str:
        """Override to return string type of logger

        Returns: str

        """
        raise NotImplementedError("Return a type string that acts as the name for the logger")

    async def main(self, message) -> bool:
        """Override to implement the logging

        Args:
            message: str the message that needs to be logged

        Returns: bool whether logging worked

        """
        raise NotImplementedError("Implement this method to log the message")

    async def log(self, message):
        """Calls the main method.

        Will be used to reformat parameters for main

        Args:
            message: str

        Returns: bool

        """
        return await self.main(message)


class CLILogger(Logger):
    """Logs to command line"""

    @staticmethod
    def type() -> str:
        """Returns 'cli' as the name of this logger

        Returns: str

        """
        return 'cli'

    async def main(self, message):
        """Simply prints the message

        Args:
            message: str Message to be logged

        Returns: bool Currently always returns True

        """
        print(message)

        return True


def get_default_loggers():
    """Returns all loggers with the logger type/id as key

    Returns:

    """
    loggers = [CLILogger]

    return {l.type(): l for l in loggers}
