from pygarl.classifiers import SVMClassifier
from pygarl.middlewares import TrimmerMiddleware, FFTMiddleware
from pygarl.plugins.train import train_classifier
import sys

dataset_dir = sys.argv[1]

# If launched directly, parse the parameters from sys
if __name__ == '__main__':
    tm = TrimmerMiddleware(threshold=300)
    fft = FFTMiddleware()

    # Create the classifier
    classifier = SVMClassifier(dataset_path=dataset_dir, verbose=True, n_jobs=8,
                               autonormalize=False, autoscale_size=500, middlewares=[tm, fft])

    # Train the classifier
    train_classifier(classifier=classifier, dataset_dir=dataset_dir, output_file="model.svm", n_jobs=8)