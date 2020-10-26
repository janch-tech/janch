import asyncio

import aiohttp


async def _run_command(shell=False,*args):
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
    return stdout.decode().strip()


async def curl(url=None):
    ret = {}

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            ret['status'] = response.status
            ret['headers'] = response.headers
            ret['html'] = await response.text()

    return ret


async def grep(filepath=None, search=None):
    output = await _run_command(False, *['grep', search, filepath])

    ret = {
        'result': output,
        'line_count': output.count('\n') + 1
    }

    return ret


async def command(command_str):
    output = await _run_command(True, *[command_str])

    return {
        'result': output
    }


def get_default_gatherers():
    return {
        'curl': {
            'params': ['url'],
            'method': curl,
            'output': ['status', 'headers', 'html']
        },
        'grep': {
            'params': ['filepath', 'search'],
            'method': grep,
            'output': ['result', 'line_count']
        },
        'command': {
            'params': ['command_str'],
            'method': command,
            'output': ['result']
        }
    }
