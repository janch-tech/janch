import json
from abc import ABC


class Formatter(ABC):

    @staticmethod
    def type() -> str:
        raise NotImplementedError("Please specify type for this formatter")

    async def header(self, params) -> str:
        raise NotImplementedError("Please specify a string header")

    async def footer(self, params) -> str:
        raise NotImplementedError("Please specify a string footer")

    async def main(self, params) -> str:
        raise NotImplementedError("Please specify a method for formatting")

    async def format(self, item, settings, gathered, inspected):
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

        body = await self.main(params)

        return body


class JSONFormatter(Formatter):

    async def header(self, params) -> str:
        pass

    async def footer(self, params) -> str:
        pass

    @staticmethod
    def type() -> str:
        return 'json'

    async def main(self, params) -> str:
        return json.dumps(params)


class SimpleFormatter(Formatter):

    async def header(self, params) -> str:
        return "|" + '|'.join(self.DIM.keys()) + '|'

    async def footer(self, params) -> str:
        return "Thanks"

    def __init__(self):
        self.DIM = {
            'item': 32,
            'type': 8,
            'field': 16,
            'expected': 32,
            'actual': 32,
            'match': 5,
            'error': 5,

        }

    @staticmethod
    def type() -> str:
        return 'simple'

    def _fit(self, size, txt):
        # Length
        l = len(txt)

        # dimension of field
        d = size

        # number of spaces to append
        s = d - l if l <= d else 0

        # ellipsis
        e = '..' if l > d else ''

        return txt[0:(l if l <= d else (d - len(e)))] + e + ' ' * s

    def _create_table(self, rows):
        ret = ''
        for row in rows:
            ret += f"|"
            for k, v in self.DIM.items():
                ret += self._fit(v, str(row[k]))
                ret += '|'

            ret += '\n'
        return ret

    async def main(self, params) -> str:
        rows = []

        for k, v in params['settings']['inspect'].items():
            row = {
                'item': params['item'],
                'type': params['settings']['gather']['type'],
                'field': k,
                'expected': v['value'] if isinstance(v, dict) else v,
                'actual': params['actuals'][k],
                'match': params['matches'][k],
                'error': params['gathered']['error'] is not None
            }

            rows.append(row)

        return self._create_table(rows)


class TabularFormatter(Formatter):

    async def header(self, params) -> str:
        pass

    async def footer(self, params) -> str:
        pass

    @staticmethod
    def type() -> str:
        return 'tabular'

    async def main(self, params) -> str:
        item = params['item']
        gathered = params['gathered']
        expecteds = params['expecteds']
        actuals = params['actuals']
        matches = params['matches']

        return f"{item}" \
            f"|{gathered['error']}" \
            f"|{expecteds or ''}" \
            f"|{actuals or ''}" \
            f"|{matches or ''}"


class FriendlyFormatter(Formatter):

    async def header(self, params) -> str:
        pass

    async def footer(self, params) -> str:
        pass

    @staticmethod
    def type() -> str:
        return 'friendly'

    async def main(self, params) -> str:
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

        return final


def get_default_formatters():
    formatters = [JSONFormatter, FriendlyFormatter, TabularFormatter, SimpleFormatter]

    return {f.type(): f for f in formatters}
