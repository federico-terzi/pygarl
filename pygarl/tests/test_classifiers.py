import unittest
import shutil
from pygarl.classifiers import SVMClassifier
from pygarl.mocks import *
from pygarl.base import *


class SVMClassifierTestCase(unittest.TestCase):
    """
    Tests to check SVMClassifier consistency.
    In order to test the classifier, this test will try to implement
    a XOR gate using the classifier.
    """

    def setUp(self):
        # Create a test directory if it doesn't exists
        if not os.path.exists("test_dir_svm_classifier"):
            os.makedirs("test_dir_svm_classifier")

        # Create the samples with the 4 possibilities of the XOR gate
        sample1 = Sample(data=[[1], [1]], gesture_id="0")
        sample2 = Sample(data=[[0], [0]], gesture_id="0")
        sample3 = Sample(data=[[1], [0]], gesture_id="1")
        sample4 = Sample(data=[[0], [1]], gesture_id="1")


        # Save the samples in the test directory
        sample1.save_to_file(os.path.join("test_dir_svm_classifier", "0_1.txt"))
        sample2.save_to_file(os.path.join("test_dir_svm_classifier", "0_2.txt"))
        sample3.save_to_file(os.path.join("test_dir_svm_classifier", "1_1.txt"))
        sample4.save_to_file(os.path.join("test_dir_svm_classifier", "1_2.txt"))

        # Initialize an AbstractClassifier
        self.classifier = SVMClassifier(dataset_path="test_dir_svm_classifier", test_size=0.5)

    def tearDown(self):
        # Destroy the test directory
        shutil.rmtree("test_dir_svm_classifier")

        # Destroy the AbstractClassifier
        self.classifier = None

    def test_load_samples_loaded_correctly(self):
        # Load the samples
        self.classifier.load()

        # Test if samples has been loaded correctly

        # Check there are 2 0s and 2 1s
        self.assertEqual(len(list(filter(lambda x: x == 0, self.classifier.y_data))), 2)
        self.assertEqual(len(list(filter(lambda x: x == 1, self.classifier.y_data))), 2)

        # Convert to list from numpy array
        x_data_as_list = map(lambda x: x.tolist(), self.classifier.x_data)

        self.assertIn([1, 1], x_data_as_list)
        self.assertIn([1, 0], x_data_as_list)
        self.assertIn([0, 1], x_data_as_list)
        self.assertIn([0, 0], x_data_as_list)

        # Test if gestures ids has been loaded correctly
        self.assertIn("0", self.classifier.gestures)
        self.assertIn("1", self.classifier.gestures)

    def test_train_model(self):
        self.classifier.load()

        # Load samples multiple times to have a large dataset
        for n in range(100):
            self.classifier.load_samples_data()

        self.assertGreater(self.classifier.train_model(), 0.9)

    def test_predict(self):
        self.classifier.load()

        # Load samples multiple times to have a large dataset
        for n in range(100):
            self.classifier.load_samples_data()

        self.assertGreater(self.classifier.train_model(), 0.9)

        test_sample1 = Sample(data=[[1], [1]])
        test_sample2 = Sample(data=[[1], [0]])

        self.assertEqual(self.classifier.predict(test_sample1), "0")
        self.assertEqual(self.classifier.predict(test_sample2), "1")

    def test_save_model_before_training_should_fail(self):
        self.assertRaises(ValueError, self.classifier.save_model, "path")

    def test_save_and_load_model(self):
        # Load and train the model
        self.classifier.load()

        # Load samples multiple times to have a large dataset
        for n in range(100):
            self.classifier.load_samples_data()

        self.assertGreater(self.classifier.train_model(), 0.9)

        model_path = os.path.join("test_dir_svm_classifier", "model.svm")

        # Save the model
        self.classifier.save_model(model_path)

        # Create a new classifier and load the saved model
        new_classifier = SVMClassifier(model_path=model_path)

        # Load the model from the saved model
        new_classifier.load()

        # Check if the loaded model works correctly
        test_sample1 = Sample(data=[[1], [1]])
        test_sample2 = Sample(data=[[1], [0]])

        self.assertEqual(new_classifier.predict(test_sample1), "0")
        self.assertEqual(new_classifier.predict(test_sample2), "1")


if __name__ == '__main__':
    unittest.main()
