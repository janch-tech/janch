from abc import ABC


class Inspector(ABC):

    def __init__(self, settings):
        self.settings = settings

    @staticmethod
    def type() -> str:
        raise NotImplementedError("Specify a type for this inspector")

    async def match(self, target, expression) -> bool:
        raise NotImplementedError("Use the parameters to assert that target matches expression")

    async def inspect(self, target, expression):
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
        return 'equals'

    async def match(self, target, check_with) -> bool:
        return target == check_with


class RegexInspector(Inspector):
    """Checks regex match"""

    @staticmethod
    def type() -> str:
        return 'regex'

    async def match(self, target, expression) -> bool:
        import re
        pattern = re.compile(expression)
        matches = pattern.match(repr(target))
        return matches is not None


def get_default_inspectors():
    inspectors = [EqualsInspector, RegexInspector]

    return {i.type(): i for i in inspectors}
