import asyncio

from janch.src import context


def info(message):
    print(message)


async def inspect(gathered, settings):
    info("Inspecting")

    ret = {}

    type = 'equals'
    for name, value in settings.items():
        inspected = await context.inspectors[type](value, gathered[name])
        ret[name] = inspected

    info("Inspection Completed")

    return ret


async def gather(settings):
    info("Gathering")
    type = settings["type"]
    gatherer = context.gatherers[type]

    gathered = None

    if gatherer:
        params = {p:settings[p] for p in gatherer['params']}
        method = gatherer['method']
        output = gatherer['output']

        gathered = await method(**params)

        for k,v in gathered.items():
            assert k in output

    info("Gathering Completed")

    return gathered




async def start_item(item, settings):
    info(f"Starting {item}")
    gathered = await gather(settings['gather'])
    info(await inspect(gathered, settings['inspect']))

    info("Complete")


async def start():
    config = context.config
    await asyncio.gather(*(start_item(item, settings) for item, settings in config.items()))
