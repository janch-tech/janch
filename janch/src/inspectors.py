async def equals(target, check_with):
    return {
        'expected': target,
        'actual': check_with,
        'match': target == check_with,
        'other':{}
    }


async def regex(target, expression):
    import re
    pattern=re.compile(expression)
    matches = pattern.match(target)
    if matches is None:
        return {
            'expected': expression,
            'actual': None,
            'match': False,
            'other':{}
        }
    else:
        return {
            'expected': expression,
            'actual': matches.group(),
            'match': True,
            'other': {
                k:matches.group(k) for k in range(1, 1+len(matches.groups()))
            }
        }







def get_default_inspectors():
    return {
        'equals': equals,
        'regex': regex
    }
