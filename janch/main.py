import asyncio
from typing import Callable, List, Dict

from janch.lib import *


def init(config,
         gatherers: List[Callable[[dict], dict]] = None,
         inspectors: List[Callable[[dict], dict]] = None,
         actors: List[Callable[[dict], dict]] = None,
         loggers: List[Callable[[dict], dict]] = None):

    context.config.update(config)
    context.gatherers.update(get_default_gatherers())
    context.inspectors.update(get_default_inspectors())
    context.loggers.update(get_default_loggers())
    context.actors.update(get_default_actors())

    context.gatherers.update(gatherers or {})
    context.inspectors.update(inspectors or {})
    context.actors.update(actors or {})
    context.loggers.update(loggers or {})


def update_gatherers(gatherer: Dict[str, Callable[[dict], dict]]):
    context.gatherers.update(gatherer)


def update_inspectors(gatherer: Dict[str, Callable[[dict], dict]]):
    context.gatherers.update(gatherer)


def update_actors(gatherer: Dict[str, Callable[[dict], dict]]):
    context.gatherers.update(gatherer)


def update_loggers(gatherer: Dict[str, Callable[[dict], dict]]):
    context.gatherers.update(gatherer)


def start():
    asyncio.run(engine.start())
