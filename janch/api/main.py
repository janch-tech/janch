import asyncio
from typing import Callable, List, Dict

from janch.factories import *
from janch.utils import *


def init(config, environment,
         gatherers: List[Callable[[dict], dict]] = None,
         inspectors: List[Callable[[dict], dict]] = None,
         actors: List[Callable[[dict], dict]] = None,
         loggers: List[Callable[[dict], dict]] = None):
    context.gatherers.update(get_default_gatherers())
    context.inspectors.update(get_default_inspectors())
    context.formatters.update(get_default_formatters())
    context.loggers.update(get_default_loggers())

    context.config.update(config)
    context.gatherers.update(gatherers or {})
    context.inspectors.update(inspectors or {})
    context.loggers.update(actors or {})
    context.formatters.update(loggers or {})
    context.environment.update(environment)


def update_gatherers(gatherer: Dict[str, Callable[[dict], dict]]):
    context.gatherers.update(gatherer)


def update_inspectors(gatherer: Dict[str, Callable[[dict], dict]]):
    context.gatherers.update(gatherer)


def update_loggers(logger: Dict[str, Callable[[dict], dict]]):
    context.loggers.update(logger)


def update_formatters(formatter: Dict[str, Callable[[dict], dict]]):
    context.formatters.update(formatter)


def start():
    try:
        asyncio.run(engine.start())
    except Exception as e:
        raise e
