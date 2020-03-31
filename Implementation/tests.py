# The tests can both be run with python and pytest.
import unittest
import os
import Discretizedata
import pathlib

GRAPH_DATA_PATH_TEST = pathlib.Path.cwd() / 'Movielens_data' / 'graphtest.csv'
RATING_PATH_TEST = pathlib.Path.cwd() / 'Movielens_data' / 'ratingtest.csv'

# The test class for graph methods.
class TestDiscretizedata(unittest.TestCase):
    """ This class contains tests for the functions in Discretizedata.py."""


    RATING_DATA = ["userId,movieId,rating,timestamp","1,296,5.0,1147880044","1,306,3.5,1147868817","1,307,5.0,1147868828","1,665,5.0,1147878820"]

    with open(RATING_PATH_TEST, 'w', newline='') as writer:
        for line in RATING_DATA:
            writer.write(line + os.linesep)

    def test_disc_rating_data(self):
        """ Tests the disc_rating_data() function by using the first 5 lines
         in the ratings.csv file"""
        expected_value = [
            "M:296,U:1,5.0\n",
            "M:306,U:1,3.5\n",
            "M:307,U:1,5.0\n",
            "M:665,U:1,5.0\n"
        ]


        Discretizedata.disc_rating_data(RATING_PATH_TEST, GRAPH_DATA_PATH_TEST, None)
        with open(GRAPH_DATA_PATH_TEST, 'r') as reader:
            graph_data = reader.readlines()
        os.remove(RATING_PATH_TEST)
        os.remove(GRAPH_DATA_PATH_TEST)
        self.assertEqual(graph_data, expected_value)

if __name__ == "__main__":
    unittest.main()
