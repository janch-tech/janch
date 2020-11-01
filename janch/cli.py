import click
import yaml
from dotenv.main import dotenv_values

from janch.api.info import *
from janch.api.main import start, init
from janch.utils.display import FixedWidth

dotenv_path = '.env'


@click.group(invoke_without_command=False)
def main():
    "Janch is a system checker configured using YAML"


@click.argument('file', type=click.File('r'))
@click.option('--item', type=str, required=False, help="Name of the item key from the yml file")
@main.command()
def run(file, item):
    """Run janch using a defined yaml file"""
    context_dict = yaml.load(file.read(), Loader=yaml.SafeLoader)

    # import json
    # print(json.dumps(context_dict))

    if item:
        selected_item = {item: context_dict.get(item)} if item in context_dict else None
    else:
        selected_item = context_dict

    if selected_item:
        init(selected_item
             , dotenv_values(dotenv_path))
        start()
    else:
        click.echo(f"Item {item} not found")
        exit()


@main.group(invoke_without_command=False)
def utils():
    "Show info about some utilities"


def _utils_info_prep(things_with_docs: dict):
    columns = {
        'type': 16,
        'description': 64
    }

    display = FixedWidth(columns)

    for gType, gClass in things_with_docs.items():
        display.add_row({"type": gType, "description": gClass.__doc__.split('\n')[0]})

    return display.get_header(), display.format()


@utils.command()
def gatherers():
    "Show information about all the gatherers"
    columns = {
        'type': 16,
        'description': 64,
        'params': 32,
        'output': 32
    }

    display = FixedWidth(columns)

    for gType, gClass in get_all_gatherers().items():
        display.add_row({
            "type": gType,
            "description": gClass.__doc__.split('\n')[0],
            "params": ','.join(gClass.get_input_fields()),
            "output": ','.join(gClass.get_output_fields())
        })

    click.echo(display.get_header())
    click.echo(display.format())


@utils.command()
def inspectors():
    "Show information about all the inspectors"
    type_and_class = get_all_inspectors()
    header, body = _utils_info_prep(type_and_class)
    click.echo(header)
    click.echo(body)


@utils.command()
def loggers():
    "Show information about all the loggers"
    type_and_class = get_all_loggers()
    header, body = _utils_info_prep(type_and_class)
    click.echo(header)
    click.echo(body)


@utils.command()
def formatters():
    """Show information about all the formatters"""
    type_and_class = get_all_formatters()
    header, body = _utils_info_prep(type_and_class)
    click.echo(header)
    click.echo(body)
