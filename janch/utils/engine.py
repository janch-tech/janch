"""Contains the main logic of Janch
"""

import asyncio

from janch.utils import context
from janch.utils.constants import NO_ERROR

_state = {
    'is_header_logged': False
}


def debug(message):
    """Temporarily placed for enabling and disabling debugging

    Will be replaced by logging library later
    """

    (f"*** {message} *** ")


async def inspect(gathered, settings):
    """Runs inspection on gathered data. Loads the inspector based on the settings

    Args:
        gathered: dict
        settings: dict with settings from the inspect section of the config yml

    Returns: dict containing results of the inspection

    """
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
    """Use the settings to gather information. Use the settings type to use the
    right gatherer class

    Args:
        settings: dict representing gather related settings from the config yml

    Returns: dict gathered data

    """
    debug("Gathering")
    type = settings.get("type") or "http"
    gatherer = context.gatherers.get(type)

    gathered = None

    if gatherer:
        gathered = await gatherer(settings).gather()

    debug("Gathering Completed")

    return gathered


async def furnish(item, settings, gathered, inspected):
    """Load the formatter to format the results of gathering and inspection

    Args:
        item: str The name of the item from the yml
        settings: dict The full settings
        gathered: dict The gathered information
        inspected: dict The inspected information

    Returns: str blob that be printed or logged

    """
    debug("Formatting")
    type = 'simple'
    formatter = context.formatters[type]

    if formatter:
        instance = formatter()
        formatted = await instance.format(item, settings, gathered, inspected)

        return formatted

    debug("Formatting Completed")


async def log(formatted):
    """Log the formatted data

    Args:
        formatted: str

    Returns: bool

    """

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
        settings.update({'inspect': {}})

    if not 'error' in settings.get('inspect'):
        settings['inspect'].update({'error': NO_ERROR})


async def start_item(item, settings):
    """Runs Janch process on a specific item

    Args:
        item: str name of the item
        settings: dict configuration of the item

    Returns:

    """
    debug(f"Starting {item}")

    _set_up_default_item_settings(settings)

    gathered = await gather(settings['gather'])
    inspected = await inspect(gathered, settings.get('inspect', {}))
    header, body = await furnish(item, settings, gathered, inspected)

    if not _state.get('is_header_logged'):
        header_logged = await log(header)
        _state.update({'is_header_logged': True})

    logged = await log(body)

    debug("Complete")


async def start():
    """Called to start the Janch process

    Returns:

    """
    config = context.config
    await asyncio.gather(*(start_item(item, settings) for item, settings in config.items()))
