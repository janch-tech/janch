import click
from yaml import load

from janch.main import start, init


@click.command()
@click.argument('file', type=click.File('r'))
def main(file):
    "Janch is a system checker configured using YAML"
    content_dict=load(file.read())
    init(content_dict)
    start()



