"""The main module for pieces of Janch
"""
import asyncio
from typing import Dict

from janch.components import *
from janch.components.formatters import Formatter
from janch.components.gatherers import Gatherer
from janch.components.inspectors import Inspector
from janch.components.loggers import Logger
from janch.utils import *


def init(config: dict, environment: Dict[str, str],
         gatherers: Dict[str, Gatherer] = None,
         inspectors: Dict[str, Inspector] = None,
         formatters: Dict[str, Formatter] = None,
         loggers: Dict[str, Logger] = None):
    """Initialize Janch by passing before using it programmatically

    Args:
        config: dict representation of the Janch yml
        environment: dict representing environment variables from dotenv
        gatherers: dict of the form {str : Gatherer}
        inspectors: dict of the form {str : Inspector}
        formatters: dict of the form {str : Formatter}
        loggers: dict of the form {str : Logger}

    Returns:

    """
    context.gatherers.update(get_default_gatherers())
    context.inspectors.update(get_default_inspectors())
    context.formatters.update(get_default_formatters())
    context.loggers.update(get_default_loggers())

    context.config.update(config)
    context.gatherers.update(gatherers or {})
    context.inspectors.update(inspectors or {})
    context.loggers.update(loggers or {})
    context.formatters.update(formatters or {})
    context.environment.update(environment)


def update_gatherers(gatherer: Dict[str, Gatherer]):
    """Replace or add a Gatherer. The key should be gatherer type str

    Args:
        gatherer: dict

    Returns:

    """
    context.gatherers.update(gatherer)


def update_inspectors(inspector: Dict[str, Inspector]):
    """Replace or add a Inspector. The key should be inspector type

    Args:
        inspector: dict

    Returns:

    """
    context.inspectors.update(inspector)


def update_loggers(logger: Dict[str, Logger]):
    """Replace or add a Logger. The key should be logger type

    Args:
        logger: dict

    Returns:

    """
    context.loggers.update(logger)


def update_formatters(formatter: Dict[str, Formatter]):
    """Replace or add a Formatter. The key should be formatter type

    Args:
        formatter: dict

    Returns:

    """
    context.formatters.update(formatter)


def start():
    """Start the Janch after it has been initialized or with default settings
    Returns:

    """
    try:
        asyncio.run(engine.start())
    except Exception as e:
        raise e
