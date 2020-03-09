# The tests can both be run with python and pytest.
import unittest
import os
import Discretizedata

# The test class for graph methods.
class TestDiscretizedata(unittest.TestCase):
    """ This class contains tests for the functions in Discretizedata.py."""
    RATING_DATA = [
        "userId,movieId,rating,timestamp",
        "1,296,5.0,1147880044",
        "1,306,3.5,1147868817",
        "1,307,5.0,1147868828",
        "1,665,5.0,1147878820",
        "1,899,3.5,1147868510",
        "1,1088,4.0,1147868495",
        "1,1175,3.5,1147868826",
        "1,1217,3.5,1147878326",
        "1,1237,5.0,1147868839"
    ]

    with open(Discretizedata.RATINGPATH, 'w') as writer:
        for line in RATING_DATA:
            writer.write(line + os.linesep)

    def test_disc_rating_data(self):
        """ Tests the disc_rating_data() method by using the first 10 lines
         in the ratings.csv file"""
         # expected_value =  (MovieId, UserId, Rating)
        expected_value = "296,1,5.0\n"
        graph_data = None
        Discretizedata.disc_rating_data()
        with open(Discretizedata.GRAPH_DATA_PATH, 'r') as reader:
            graph_data = reader.readlines()
        self.assertEqual(graph_data[1], expected_value)

if __name__ == "__main__":
    unittest.main()
