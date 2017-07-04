import unittest
import scipy as sp
from pygarl.abstracts import *
from pygarl.predictors import *
from pygarl.mocks import *
from pygarl.base import *

# To execute tests, go to the project main directory and type:
# python -m unittest discover


class HighestAxisPredictorTestCase(unittest.TestCase):
    """
    Tests to check HighestAxisPredictor behaviour
    """
    def setUp(self):
        # Initialize the HighestAxisPredictor
        self.predictor = HighestAxisPredictor()

    def tearDown(self):
        # Destroy the predictor
        self.predictor = None

    def test_predict_only_one_sample_frame(self):
        sample = Sample(data=[[1, 2, 3, 2]])

        self.assertEqual(self.predictor.predict(sample), "2")

    def test_predict_only_one_sample_frame_with_negatives(self):
        sample = Sample(data=[[1, -2, -3, -2]])

        self.assertEqual(self.predictor.predict(sample), "0")

    def test_predict_absolute_values_option(self):
        sample = Sample(data=[[1, -2, -3, -2]])

        # Set the absolute values option
        self.predictor.absolute_values = True

        self.assertEqual(self.predictor.predict(sample), "2")

    def test_predict_multiple_frames(self):
        sample = Sample(data=[[2, 3, 3, 2], [0, 0, 3, 1]])

        self.assertEqual(self.predictor.predict(sample), "2")

    def test_predict_empty_sample_should_raise_error(self):
        sample = Sample(data=[[]])

        self.assertRaises(ValueError, self.predictor.predict, sample)

if __name__ == '__main__':
    unittest.main()
