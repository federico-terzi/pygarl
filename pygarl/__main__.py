import click  # Use the click library to provide a CLI interface
import importlib


@click.group()
def cli():
    pass


@cli.command()
def record():
    """
    Record new samples
    """
    click.echo("Record")


@cli.command()
@click.argument('example_name')
def example(example_name):
    """
    Run an example from pygarl.examples
    """
    # Launch the example
    importlib.import_module("pygarl.examples." + example_name)


if __name__ == '__main__':
    cli()
