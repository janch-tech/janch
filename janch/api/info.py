"""Contains methods to get access to all factory methods that make the janch yml possible"""
from janch.components import *


def get_all_gatherers() -> dict:
    """Get all gatherer classes
    Returns: dict with gatherer type names are keys and gatherer classes as values

    """
    return get_default_gatherers()


def get_all_inspectors() -> dict:
    """Get all inspector classes
    Returns: dict with inspector type names are keys and inspector classes as values

    """
    return get_default_inspectors()


def get_all_loggers():
    """Get all logger classes
    Returns: dict with logger type names are keys and logger classes as values

    """
    return get_default_formatters()


def get_all_formatters():
    """Get all formatter classes
    Returns: dict with formatter type names are keys and formatter classes as values

    """
    return get_default_formatters()
