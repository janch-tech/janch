import asyncio

from janch.src import context


def debug(message):
    (f"*** {message} *** ")



async def inspect(gathered, settings):
    debug("Inspecting")

    ret = {}

    DEFAULT = 'regex'
    for name, details in settings.items():

        if isinstance(details, dict):
            type = details.get('type') or DEFAULT
            value = details.get('value')
        elif not isinstance(details,str):
            type = 'equals'
            value = details
        else:
            type = DEFAULT
            value = details

        inspected = await context.inspectors[type](gathered[name], value)
        ret[name] = inspected

    debug("Inspection Completed")

    return ret


async def gather(settings):
    debug("Gathering")
    type = settings.get("type") or "curl"
    gatherer = context.gatherers[type]

    gathered = None

    if gatherer:
        params = {p:settings[p] for p in gatherer['params']}
        method = gatherer['method']
        output = gatherer['output']

        gathered = await method(**params)

        for k,v in gathered.items():
            assert k in output

    debug("Gathering Completed")

    return gathered


async def log(item, inspected, settings):
    debug("Logging")
    type=settings.get('type') or 'cli'
    logger = context.loggers[type]

    if logger:
        params = inspected
        method = logger['method']

        logger = await method(item, params)

    debug("Logging Completed")


async def start_item(item, settings):
    debug(f"Starting {item}")
    gathered = await gather(settings['gather'])
    inspected=await inspect(gathered, settings['inspect'])
    logged=await log(item, inspected, settings.get('log') or {})

    debug("Complete")


async def start():
    config = context.config
    await asyncio.gather(*(start_item(item, settings) for item, settings in config.items()))
