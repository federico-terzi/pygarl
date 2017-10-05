from pygarl.classifiers import MLPClassifier, SVMClassifier
from pygarl.middlewares import AbsoluteScaleMiddleware, TrimmerMiddleware
from pygarl.plugins.train import train_classifier


def train(dataset_dir, output_file, n_jobs=1):
    """
    Used to train the knock sensor data.
    Train an MLP model from the given dataset and save it to a file.
    """

    tm = TrimmerMiddleware(threshold=300)

    # Create the classifier
    classifier = SVMClassifier(dataset_path=dataset_dir, verbose=True, n_jobs=n_jobs,
                               autonormalize=False, autoscale_size=50, middlewares=[tm])

    # Train the classifier
    train_classifier(classifier=classifier, dataset_dir=dataset_dir, output_file=output_file, n_jobs=n_jobs)
