import asyncio

import aiohttp


async def _run_command(*args):
    """
    Example from https://asyncio.readthedocs.io/en/latest/subprocess.html

    :param args:
    :return:
    """
    # Create subprocess
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

    output = await _run_command('grep', search, filepath)

    ret= {
        'result': output,
        'line_count': output.count('\n')+1
    }

    print(ret)
    return ret


def get_default_gatherers():
    return {
        'curl': {
            'params': ['url'],
            'method': curl,
            'output': ['status', 'headers', 'html']
        },
        'grep': {
            'params': ['filepath','search'],
            'method': grep,
            'output': ['result', 'line_count']
        }
    }
