from __future__ import print_function
from pygarl.classifiers import SVMClassifier, MLPClassifier
import sys


def train_classifier(classifier, dataset_dir, output_file, n_jobs=1, **kwargs):
    """
    Train a model using the passed classifier from the given dataset and save it to a file.
    
    :param classifier: Classifier used to create a model
    :param dataset_dir: Path of the dataset directory containing the samples
    :param output_file: Output file of the model 
    """
    # Load the data
    print("Loading the data...", end="")

    classifier.load()
    print("LOADED!")

    print("Training the model...")

    # Train the model and obtain the score
    score = classifier.train_model()

    print("FINAL SCORE:", score)

    print("Saving the model to the output file:", output_file)

    classifier.save_model(output_file)

    print("DONE")


def train_svm_classifier(dataset_dir, output_file, n_jobs=1):
    """
    Train an SVM model from the given dataset and save it to a file.
    """
    # Create the classifier
    classifier = SVMClassifier(dataset_path=dataset_dir, verbose=True, n_jobs=n_jobs,
                               autoscale_size=50)

    # Train the classifier
    train_classifier(classifier=classifier, dataset_dir=dataset_dir, output_file=output_file, n_jobs=n_jobs)


def train_mlp_classifier(dataset_dir, output_file, n_jobs=1):
    """
    Train an MLP model from the given dataset and save it to a file.
    """
    # Create the classifier
    classifier = MLPClassifier(dataset_path=dataset_dir, verbose=True, n_jobs=n_jobs,
                               autonormalize=True, autoscale_size=15)

    # Train the classifier
    train_classifier(classifier=classifier, dataset_dir=dataset_dir, output_file=output_file, n_jobs=n_jobs)


# If launched directly, parse the parameters from sys
if __name__ == '__main__':
    train_svm_classifier(sys.argv[0], sys.argv[1], 8)
