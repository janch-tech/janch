import click
import yaml
from dotenv.main import dotenv_values

from janch.api.main import start, init

dotenv_path = '.env'


@click.group(invoke_without_command=False)
def main():
    "Janch is a system checker configured using YAML"


@click.argument('file', type=click.File('r'))
@main.command()
def run(file):
    "Run janch using a defined yaml file"
    content_dict = yaml.load(file.read(), Loader=yaml.SafeLoader)
    init(content_dict, dotenv_values(dotenv_path))
    start()


@main.group(invoke_without_command=False)
def info():
    "Show info about some utilities"


@info.command()
def gatherers():
    "Show information about all the gatherers"
    pass


@info.command()
def inspectors():
    "Show information about all the inspectors"
    pass


@info.command()
def loggers():
    "Show information about all the loggers"
    pass
