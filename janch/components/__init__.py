"""This modules contains code that enable the components of the Janch config file

"""
from janch.components.formatters import get_default_formatters
from janch.components.gatherers import get_default_gatherers
from janch.components.inspectors import get_default_inspectors
from janch.components.loggers import get_default_loggers

__all__ = [
    'get_default_gatherers',
    'get_default_inspectors',
    'get_default_formatters',
    'get_default_loggers']
