"""Formatters set the style in which message is logged.
The formatters return a string which can be printed to cli or logged elsewhere

"""
import json
from abc import ABC

from janch.utils.constants import NO_ERROR
from janch.utils.display import FixedWidth


class Formatter(ABC):
    """Abstract base class for a formatter. You can implement a custom formatter by extending
    this class and overriding the methods
    """

    @staticmethod
    def type() -> str:
        """This is the string that identifies the specific formatter

        Returns: str

        """
        raise NotImplementedError("Please specify type for this formatter")

    async def main(self, params: dict) -> str:
        """The main formatting logic goes here.

        The params contain all the information that
        can be displayed by the formatter

        Args:
            params: dict

        Returns:

        """
        raise NotImplementedError("Please specify a method for formatting")

    async def format(self, item, settings, gathered, inspected):
        """This method creates the params for the main function

        Ideally this method should not be overridden by the extending class

        Args:
            item:
            settings:
            gathered:
            inspected:

        Returns:

        """
        params = {
            'item': item,
            'settings': settings,
            'gathered': gathered,
            'inspected': inspected,
            'expecteds': settings['inspect'],
            'actuals': {},
            'matches': {},
            'inspect_count': 0,
            'match_count': 0,
            'match_percent': 0
        }

        for k, v in inspected.items():
            if v is not None:
                params['actuals'][k] = v['actual']
                params['matches'][k] = v['match']

                params['match_count'] += 1 if v['match'] else 0
                params['inspect_count'] += 1

        params['match_percent'] = round(params['match_count'] * 1.0 / params['inspect_count'], 2)

        header, body = await self.main(params)

        return header, body


class JSONFormatter(Formatter):
    """Formats everything as a single JSON"""

    @staticmethod
    def type() -> str:
        """Return 'json'

        Returns: str

        """
        return 'json'

    async def main(self, params):
        """Simply formats the params as JSON using the json library

        Args:
            params: dict

        Returns: None, str

        """
        return None, json.dumps(params)


class SimpleFormatter(Formatter):
    """Easy to read format"""

    DIM = {
        'item': 32,
        'type': 8,
        'field': 16,
        'expected': 32,
        'actual': 32,
        'match': 6,
        'error': 6,

    }

    def __init__(self):
        self.displayer = FixedWidth(SimpleFormatter.DIM)

    @staticmethod
    def type() -> str:
        """Returns 'simple' as the name of this formatter

        Returns: str

        """
        return 'simple'

    async def main(self, params):
        """Format the results in a simple aligned tabular format

        Columns: item, type, field, expected, actual, match, error

        Args:
            params:

        Returns:

        """
        for k, v in params['settings']['inspect'].items():
            row = {
                'item': params['item'],
                'type': params['settings']['gather']['type'],
                'field': k,
                'expected': v['value'] if isinstance(v, dict) else v,
                'actual': params['actuals'].get(k),
                'match': params['matches'].get(k) or False,
                'error': params['gathered']['error'] != NO_ERROR
            }

            self.displayer.add_row(row)

        return self.displayer.get_header(), self.displayer.format()


class PipeDelimited(Formatter):
    """Pipe delimited format"""

    @staticmethod
    def type() -> str:
        """Returns 'pipe' as the name of this formatter

        Returns: str

        """
        return 'pipe'

    async def main(self, params):
        """Displays information in a pipe delimited format

        Args:
            params:

        Returns:

        """
        item = params['item']
        gathered = params['gathered']
        expecteds = params['expecteds']
        actuals = params['actuals']
        matches = params['matches']

        return None, f"{item}" \
            f"|{gathered['error']}" \
            f"|{expecteds or ''}" \
            f"|{actuals or ''}" \
            f"|{matches or ''}"


class FriendlyFormatter(Formatter):
    """Natural language format"""

    @staticmethod
    def type() -> str:
        """Returns 'friendly' as the name of this formatter

        Returns: str

        """
        return 'friendly'

    async def main(self, params):
        """Displays information in a friendly format with the information spanning multiple lines

        Args:
            params: dict

        Returns:

        """
        item = params['item']
        gathered = params['gathered']
        expecteds = params['expecteds']
        actuals = params['actuals']
        match_count = params['match_count']
        inspect_count = params['inspect_count']
        settings = params['settings']

        final = f"In {item},"

        def level(msg, n):
            return '\n' + ' ' * (n * 2) + msg

        final += level("Overall Status:", 1)

        final += level(f"Errors: {gathered['error'] is not None}", 2)
        final += level(f"Matches: {match_count}/{inspect_count}", 2)

        if gathered['error']:
            final += level(
                f"Error occured on attempting to read {item} using {settings['gather']}",
                1)
        else:
            final += level(
                f"We expected the following:", 1)

            for k, v in expecteds.items():
                final += level(
                    k + "=" + str(v), 2
                )

            final += level(
                f"We actually detected the following:", 1)

            for k, v in actuals.items():
                final += level(
                    k + "=" + str(v), 2
                )

        return None, final


def get_default_formatters():
    """Returns all formatters with the formatter type/id as key
    """
    formatters = [JSONFormatter, FriendlyFormatter, PipeDelimited, SimpleFormatter]

    return {f.type(): f for f in formatters}
