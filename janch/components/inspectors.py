"""Inspectors are classes that compare and check the gathered data
"""
from abc import ABC


class Inspector(ABC):
    """Abstract base class for all Inspector classes

    Inspectors are like comparators

    """

    def __init__(self, settings):
        """Pass the dict form of the inspect section from the config file

        Args:
            settings: dict
        """
        self.settings = settings

    @staticmethod
    def type() -> str:
        """This is the string that identifies the specific inspector

        Returns: str

        """
        raise NotImplementedError("Specify a type for this inspector")

    async def match(self, target, expression) -> bool:
        """This is the method that needs to be overridden to implement an Inspector

        Args:
            target: str The value that needs to be inspected. Gathered by gatherer
            expression: str The value that needs to be compared with. Specified in config

        Returns:

        """
        raise NotImplementedError("Use the parameters to assert that target matches expression")

    async def inspect(self, target, expression):
        """Creates parameters for the match method and creates return dic

        Args:
            target: str The value that needs to be inspected. Gathered by gatherer
            expression: str The value that needs to be compared with. Specified in config

        Returns: dict with 'expected', 'actual' and 'match' as keys

        """
        is_match = await self.match(target, expression)

        return {
            'expected': expression,
            'actual': repr(target).strip("\'\""),
            'match': is_match,
        }


class EqualsInspector(Inspector):
    """Checks a==b"""

    @staticmethod
    def type() -> str:
        """Return 'equals'

        Returns: str

        """
        return 'equals'

    async def match(self, target, check_with) -> bool:
        """Checks if the two parameters and equal using ==

        Args:
            target: str The gathered data
            check_with: str

        Returns: bool

        """
        return target == check_with


class RegexInspector(Inspector):
    """Checks regex match"""

    @staticmethod
    def type() -> str:
        """Return 'regex'

        Returns: str

        """
        return 'regex'

    async def match(self, target, expression) -> bool:
        """Checks if the target matches a given regular expression

        Args:
            target: Gathered data
            expression: specified in YML

        Returns: bool

        """
        import re
        pattern = re.compile(expression)
        matches = pattern.match(target)
        return matches is not None


def get_default_inspectors():
    """Returns all inspectors with the inspector type/id as key

    Returns: dict[str: Inspector]

    """
    inspectors = [EqualsInspector, RegexInspector]

    return {i.type(): i for i in inspectors}
