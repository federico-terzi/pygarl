from __future__ import print_function
from pygarl.classifiers import SVMClassifier


def train_svm_classifier(dataset_dir, output_file, n_jobs=1):
    """
    Train an SVM model from the given dataset and save it to a file.
    
    :param dataset_dir: Path of the dataset directory containing the samples
    :param output_file: Output file of the model 
    """
    # Create the classifier
    classifier = SVMClassifier(dataset_path=dataset_dir, verbose=True, n_jobs=n_jobs,
                               autonormalize=True, autoscale_size=50)

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