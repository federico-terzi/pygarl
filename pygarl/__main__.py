import click  # Use the click library to provide a CLI interface
import importlib
import os

from pygarl.plugins.plist import list_serial_ports
from pygarl.plugins.plot import plot_sample
from pygarl.plugins.record import record_new_samples, record_new_samples_stream
from pygarl.plugins.train import train_svm_classifier, train_mlp_classifier


def get_default_record_directory():
    """
    Used to generate the default user directory for saving new samples
    """
    # Get the user HOME directory
    home = os.path.expanduser("~")

    # Generate the complete path as: $HOME/dataset
    complete_path = os.path.join(home, "dataset")

    return complete_path


@click.group()
def cli():
    pass


@cli.command()
@click.option('--port', '-p', default="COM6", help="Serial Port NAME, for example COM3.")
@click.option('--dir', '-d', default=get_default_record_directory(),
              help="Target directory where samples will be saved.")
@click.option('--gesture', '-g', default="SAMPLE",
              help="Gesture ID of the recorded samples.")
@click.option('--axis', '-a', default=6, help="Number of AXIS in the signal, default 6.")
@click.option('--mode', '-m', default="discrete", help="Recording mode. You can choose between discrete and stream.")
def record(port, dir, gesture, axis, mode):
    """
    Record new samples and saves them to file
    """
    if mode == "discrete":
        record_new_samples(port=port, gesture_id=gesture, target_dir=dir, expected_axis=axis)
    elif mode == "stream":
        record_new_samples_stream(port=port, gesture_id=gesture, target_dir=dir, expected_axis=axis)


@cli.command()
def plist():
    """
    Prints all the available serial ports
    """
    list_serial_ports()


@cli.command()
@click.option('--dir', '-d', default=get_default_record_directory(),
              help="Dataset directory where samples are saved.")
@click.option('--classifier', '-c', default="svm",
              help="Classifier used to create a model. Default is SVM. You can use svm, mlp and custom.")
@click.option('--trainer', '-t', default=None,
              help="Load a custom trainer. --classifier custom must be specified.")
@click.argument('output_file')
def train(dir, classifier, output_file, trainer):
    """
    Train a model from a dataset
    """
    # Load the appropriate method based on the specified classifier
    if classifier == "svm":
        train_svm_classifier(dir, output_file)
    elif classifier == "mlp":
        train_mlp_classifier(dir, output_file)
    elif classifier == "custom":
        if trainer is None:
            raise ValueError("If --classifier custom is used, a trainer must be specified")

        # Load the trainer
        trainer = importlib.import_module("pygarl.plugins.trainers." + trainer)

        # Train the classifier
        trainer.train(dir, output_file)
    else:
        raise ValueError("{classifier} is not a valid classifier".format(classifier=classifier))


@cli.command()
@click.option('--port', '-p', default="COM6", help="Serial Port NAME, for example COM3.")
@click.argument('example_name')
@click.argument('args', nargs=-1)
def example(port, example_name, args):
    """
    Run an example from pygarl.examples
    """
    # Load the example
    ex = importlib.import_module("pygarl.examples." + example_name)

    # Check if there are arguments, if so, get them.
    arguments = None
    if len(args) > 0:
        arguments = args[0]

    # Run the example
    ex.run_example(arguments, port=port)


@cli.command()
@click.argument('sample_file')
def plot(sample_file):
    """
    Plot the sample for the given file
    """
    plot_sample(sample_file)

if __name__ == '__main__':
    cli()
