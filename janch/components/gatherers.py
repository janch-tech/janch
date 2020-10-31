"""Gatherers are classes that collect the data from various sources
"""
import asyncio
from abc import ABC

import aiohttp

from janch.utils.constants import NO_ERROR


class Gatherer(ABC):
    """Abstract base class for all Gatherer classes
    """

    def __init__(self, settings):
        self.settings = settings

    @staticmethod
    def get_input_fields() -> list:
        """The list of fields needed for this gatherer to work

        Returns: list

        """
        raise NotImplementedError("Should be a string array of field names")

    @staticmethod
    def get_output_fields() -> list:
        """The list of fields that will be output by this gatherer

        Returns:

        """
        raise NotImplementedError("Should return an array of output fields")

    @staticmethod
    def type():
        """The gatherer type

        Returns:

        """
        raise NotImplementedError("Return name of gatherer")

    async def main(self, *args):
        """The main method that should contain the gatherer logic

        Args:
            *args: fields that should be the same as the ones in get_input_fields method

        Returns:

        """
        raise NotImplementedError("Should use the args to gather")

    async def gather(self):
        """This method prepares the parameters for the main method

        This method need not be overridden

        Returns: dict

        """
        params = [self.settings[p] for p in self.get_input_fields()]
        output = self.get_output_fields()
        method = self.main

        gathered = await method(*params)

        for k, v in gathered.items():
            assert k in output

        if not gathered.get('error'):
            gathered['error'] = NO_ERROR

        return gathered


class HttpGatherer(Gatherer):
    """Gather information from a http(s) source

    """

    @staticmethod
    def type():
        """The HttpGatherer type

        Returns: str http

        """
        return "http"

    @staticmethod
    def get_input_fields():
        """The input fields ['url']

        Returns: list

        """
        return ['url']

    @staticmethod
    def get_output_fields():
        """The output fields ['status', 'headers', 'html', 'error']

        Returns: list

        """
        return ['status', 'headers', 'html', 'error']

    async def main(self, url):
        """Makes a request to the url

        Args:
            url: str The http(s) which needs to be requested

        Returns: dict

        """
        import sys

        ret = {'error': None}

        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url, ssl=False) as response:
                    ret['status'] = response.status
                    ret['headers'] = str(response.headers)
                    ret['html'] = str(await response.text())
        except Exception as e:
            ex_type, ex_value, ex_traceback = sys.exc_info()

            ret['error'] = ex_value

        return ret


class CommandGatherer(Gatherer):
    """Execute a shell command

    """

    @staticmethod
    def type():
        """The CommandGatherer type

        Returns: str command

        """
        return "command"

    @staticmethod
    async def run_command(shell=False, *args):
        """
        Example from the following were modified
        https://asyncio.readthedocs.io/en/latest/subprocess.html
        https://docs.python.org/3/library/asyncio-subprocess.html

        :param args:
        :return:
        """

        # Create subprocess
        if shell:
            process = await asyncio.create_subprocess_shell(
                args[0],
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE)
        else:
            process = await asyncio.create_subprocess_exec(
                *args,
                # stdout must a pipe to be accessible as process.stdout
                stdout=asyncio.subprocess.PIPE)
        # Wait for the subprocess to finish
        stdout, stderr = await process.communicate()
        # Return stdout
        return stdout.decode().strip(), stderr.decode().strip() if stderr else None

    @staticmethod
    def get_input_fields():
        """The input fields ['command_str']

        Returns: list

        """
        return ['command_str']

    @staticmethod
    def get_output_fields():
        """The output fields ['result', 'error']

        Returns: list

        """
        return ['result', 'error']

    async def main(self, command_str):
        """Executes the command

        Args:
            command_str: str the shell command to be executed

        Returns: dict

        """
        output, error = await CommandGatherer.run_command(True, *[command_str])

        return {
            'result': output,
            'error': error
        }


class GrepGatherer(Gatherer):
    """Execute a grep command

    """

    @staticmethod
    def type():
        """The GrepGatherer type

        Returns: str grep

        """
        return "grep"

    @staticmethod
    def get_input_fields():
        """The input fields ['filepath', 'search']

        Returns: list

        """
        return ['filepath', 'search']

    @staticmethod
    def get_output_fields():
        """The output fields ['result', 'line_count', 'error']

        Returns: list

        """
        return ['result', 'line_count', 'error']

    async def main(self, filepath, search):
        """Greps the file in the filepath with the search string

        Args:
            filepath: str
            search: str

        Returns: dict

        """
        output, error = await CommandGatherer.run_command(False, *['grep', search, filepath])

        ret = {
            'result': output,
            'line_count': output.count('\n') + 1,
            'error': error
        }

        return ret


def get_default_gatherers():
    """Returns all the gatherers as dict

    Returns: dict[str: Gatherer]

    """
    gatherers = [HttpGatherer, GrepGatherer, CommandGatherer]

    return {c.type(): c for c in gatherers}
