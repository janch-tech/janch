import pytest
from janch.components.inspectors import EqualsInspector, RegexInspector


@pytest.mark.asyncio
async def test_equals_inspector():
    inspector = EqualsInspector({})

    target = "Hello, World!"
    expected = "Hello, World!"

    result = await inspector.inspect(target, expected)

    assert result['match'] is True
    assert result['actual'] == expected


@pytest.mark.asyncio
async def test_regex_inspector():
    inspector = RegexInspector({})

    target = "Python 3.8.10"
    regex = r"^Python 3\.\d+\.\d+$"

    result = await inspector.inspect(target, regex)

    assert result['match'] is True
    assert result['actual'] == target
