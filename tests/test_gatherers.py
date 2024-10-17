import pytest
from janch.components.gatherers import HttpGatherer, CommandGatherer, GrepGatherer


@pytest.mark.asyncio
async def test_http_gatherer():
    settings = {"url": "https://httpbin.org/status/200"}
    gatherer = HttpGatherer(settings)

    result = await gatherer.gather()

    assert result['status'] == 200
    assert result['error'] == 'NOERROR'


@pytest.mark.asyncio
async def test_command_gatherer():
    settings = {"command_str": "echo Hello, World!"}
    gatherer = CommandGatherer(settings)

    result = await gatherer.gather()

    assert result['result'] == "Hello, World!"
    assert result['error'] == 'NOERROR'


@pytest.mark.asyncio
async def test_grep_gatherer(tmp_path):
    # Create a temporary file for the test
    file_path = tmp_path / "test_file.txt"
    file_path.write_text("Hello=world\nGoodbye=earth")

    settings = {"filepath": str(file_path), "search": "="}
    gatherer = GrepGatherer(settings)

    result = await gatherer.gather()

    assert "Hello=world" in result['result']
    assert result['line_count'] == 2
    assert result['error'] == 'NOERROR'
