import click  # Use the click library to provide a CLI interface
import importlib


@click.group()
def cli():
    pass


@cli.command()
@click.option('--port', '-p', default="COM6", help="Serial Port NAME, for example COM3.")
@click.argument('target_dir')
def record(port, target_dir):
    """
    Record new samples and saves them in the passed directory 
    """
    click.echo("Record" + port)


@cli.command()
@click.option('--port', '-p', default="COM6", help="Serial Port NAME, for example COM3.")
@click.argument('example_name')
def example(port, example_name):
    """
    Run an example from pygarl.examples
    """
    # Load the example
    ex = importlib.import_module("pygarl.examples." + example_name)

    # Run the example
    ex.run_example(port=port)


if __name__ == '__main__':
    cli()
