from pygarl.classifiers import MLPClassifier, SVMClassifier
from pygarl.middlewares import AbsoluteScaleMiddleware
from pygarl.plugins.train import train_classifier


def train(dataset_dir, output_file, n_jobs=1):
    """
    Used to train the knock sensor data.
    Train an MLP model from the given dataset and save it to a file.
    """
    asm = AbsoluteScaleMiddleware()

    # Create the classifier
    classifier = SVMClassifier(dataset_path=dataset_dir, verbose=True, n_jobs=n_jobs,
                               autonormalize=True, autoscale_size=40, middlewares=[asm])

    # Train the classifier
    train_classifier(classifier=classifier, dataset_dir=dataset_dir, output_file=output_file, n_jobs=n_jobs)
