import pytest
from janch.components.formatters import SimpleFormatter, JSONFormatter


@pytest.mark.asyncio
async def test_simple_formatter():
    formatter = SimpleFormatter()

    params = {
        'item': 'command-example',
        'settings': {
            'gather': {'type': 'command'},
            'inspect': {'result': '^Python 3\\.(.*)$'}
        },
        'gathered': {'error': 'NOERROR'},
        'inspected': {'result': {'match': True, 'actual': 'Python 3.8.10'}}
    }

    header, body = await formatter.format('command-example', params['settings'], params['gathered'],
                                          params['inspected'])

    assert 'command-example' in body
    assert 'Python 3.8.10' in body


@pytest.mark.asyncio
async def test_json_formatter():
    formatter = JSONFormatter()

    params = {
        'item': 'command-example',
        'settings': {
            'gather': {'type': 'command'},
            'inspect': {'result': '^Python 3\\.(.*)$'}
        },
        'gathered': {'error': 'NOERROR'},
        'inspected': {'result': {'match': True, 'actual': 'Python 3.8.10'}}
    }

    header, body = await formatter.format('command-example', params['settings'], params['gathered'],
                                          params['inspected'])

    assert '"command-example"' in body
    assert '"Python 3.8.10"' in body
