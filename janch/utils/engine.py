import asyncio

from janch.factories.gatherers import NO_ERROR
from janch.utils import context

_state={
    'is_header_logged': False
}

def debug(message):
    (f"*** {message} *** ")


async def inspect(gathered, settings):
    debug("Inspecting")

    ret = {}

    DEFAULT = 'regex'

    for field_name, details in settings.items():

        if field_name in gathered:

            if isinstance(details, dict):
                type = details.get('type') or DEFAULT
                value = details.get('value')
            elif not isinstance(details, str):
                type = 'equals'
                value = details
            else:
                type = DEFAULT
                value = details

            inspector = context.inspectors[type](None)

            inspected = await inspector.inspect(gathered[field_name], value)
            ret[field_name] = inspected
        else:
            ret[field_name] = None

    debug("Inspection Completed")

    return ret


async def gather(settings):
    debug("Gathering")
    type = settings.get("type") or "curl"
    gatherer = context.gatherers.get(type)

    gathered = None

    if gatherer:
        gathered = await gatherer(settings).gather()

    debug("Gathering Completed")

    return gathered


async def format(item, settings, gathered, inspected):
    debug("Formatting")
    type = 'simple'
    formatter = context.formatters[type]

    if formatter:
        instance = formatter()
        formatted = await instance.format(item, settings, gathered, inspected)

        return formatted

    debug("Formatting Completed")


async def log(formatted):
    debug("Logging")
    type = 'cli'

    logger = context.loggers[type]

    if logger:
        method = logger().log

        logged = await method(formatted)

        return logged

    debug("Logging completed")



def _set_up_default_item_settings(settings):
    if not 'inspect' in settings:
        settings.update({'inspect':{}})

    if not 'error' in settings.get('inspect'):
        settings['inspect'].update({'error':NO_ERROR})

async def start_item(item, settings):
    debug(f"Starting {item}")

    _set_up_default_item_settings(settings)


    gathered = await gather(settings['gather'])
    inspected = await inspect(gathered, settings.get('inspect', {}))
    header, body = await format(item, settings, gathered, inspected)

    if not _state.get('is_header_logged'):
        header_logged = await log(header)
        _state.update({'is_header_logged':True})

    logged = await log(body)

    debug("Complete")


async def start():
    config = context.config
    await asyncio.gather(*(start_item(item, settings) for item, settings in config.items()))
