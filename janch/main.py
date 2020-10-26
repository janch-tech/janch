import asyncio
from typing import Callable, List, Dict

from janch.src import *


def init(config, environment,
         gatherers: List[Callable[[dict], dict]] = None,
         inspectors: List[Callable[[dict], dict]] = None,
         actors: List[Callable[[dict], dict]] = None,
         loggers: List[Callable[[dict], dict]] = None):
    context.gatherers.update(get_default_gatherers())
    context.inspectors.update(get_default_inspectors())
    context.loggers.update(get_default_loggers())
    context.actors.update(get_default_actors())

    context.config.update(config)
    context.gatherers.update(gatherers or {})
    context.inspectors.update(inspectors or {})
    context.actors.update(actors or {})
    context.loggers.update(loggers or {})
    context.environment.update(environment)


def update_gatherers(gatherer: Dict[str, Callable[[dict], dict]]):
    context.gatherers.update(gatherer)


def update_inspectors(gatherer: Dict[str, Callable[[dict], dict]]):
    context.gatherers.update(gatherer)


def update_actors(gatherer: Dict[str, Callable[[dict], dict]]):
    context.gatherers.update(gatherer)


def update_loggers(gatherer: Dict[str, Callable[[dict], dict]]):
    context.gatherers.update(gatherer)


def start():
    try:
        asyncio.run(engine.start())
    except Exception as e:
        pass
    finally:
        pass
