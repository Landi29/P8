# The tests can both be run with python and pytest.
import unittest
import os
import pathlib
import Discretizedata
import tet
import build_tet
import compare_tet
import Paths


GRAPH_DATA_PATH_TEST = pathlib.Path.cwd() / 'Movielens_data' / 'graphtest.csv'
RATING_PATH_TEST = pathlib.Path.cwd() / 'Movielens_data' / 'ratingtest.csv'

# The test class for graph methods.
'''
class TestDiscretizedata(unittest.TestCase):
    """ This class contains tests for the functions in Discretizedata.py."""


    RATING_DATA = ["userId,movieId,rating,timestamp"
    ,"1,296,5.0,1147880044"
    ,"1,306,3.5,1147868817"
    ,"1,307,5.0,1147868828"
    ,"1,665,5.0,1147878820"]

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
        self.assertEqual(graph_data[1:], expected_value)
        
        os.remove(RATING_PATH_TEST)
        os.remove(GRAPH_DATA_PATH_TEST)
        self.assertEqual(graph_data, expected_value)
'''

class Testtet(unittest.TestCase):
    '''
    tests for the tet class
    '''
    def test_tet_construction(self):
        '''
        test the construction of a tet
        '''
        test_objekt = tet.TET()
        self.assertIsInstance(test_objekt, tet.TET)

    def test_tet_getroot(self):
        '''
        tests getroot in tet
        '''
        username = 'u:1234'
        test_objekt = tet.TET(root=username)
        self.assertIs(test_objekt.getroot(), username)

    def test_tet_isroot1(self):
        '''
        test isroot true in tet
        '''
        username = 'u:1234'
        test_objekt = tet.TET(root=username)
        self.assertTrue(test_objekt.isroot(username))

    def test_tet_isroot2(self):
        '''
        test isroot false in tet
        '''
        username = 'u:1234'
        test_objekt = tet.TET(root=username)
        self.assertFalse(test_objekt.isroot('lars'))

    def test_tet_getchildren(self):
        '''
        test get children in tet
        '''
        username = 'u:1234'
        children = [tet.TETChild('Lars')]
        test_objekt = tet.TET(root=username, children=children)
        self.assertEqual(test_objekt.getchildren(), children)

    def test_tet_tostring1(self):
        '''
        test tostring in simple tet
        '''
        username = 'u:1234'
        test_objekt = tet.TET(root=username)
        self.assertEqual(test_objekt.tostring(), '[u:1234]')

    def test_tet_tostring2(self):
        '''
        test tostring in tet with children
        '''
        username = 'u:1234'
        children = [tet.TETChild('high', children=tet.TETChild('action'))]
        test_objekt = tet.TET(root=username, children=children)
        self.assertEqual(test_objekt.tostring(), '[u:1234,[[high,[[action]]]:1]]')

    def test_tet_tostring3(self):
        '''
        test tostring in tet with children
        '''
        username = 'u:1234'
        children = [tet.TETChild('high', children=tet.TETChild('action')),
                    tet.TETChild('high', children=tet.TETChild('action'))]
        test_objekt = tet.TET(root=username, children=children)
        self.assertEqual(test_objekt.tostring(), '[u:1234,[[high,[[action]]]:2]]')

    def test_tet_tostring4(self):
        '''
        test tostring in tet with children
        '''
        username = 'u:1234'
        children = [tet.TETChild('high', children=tet.TETChild('action')),
                    tet.TETChild('low', children=tet.TETChild('action'))]
        test_objekt = tet.TET(root=username, children=children)
        self.assertEqual(test_objekt.tostring(),
                         '[u:1234,[[high,[[action]]]:1,[low,[[action]]]:1]]')

    def test_tet_count_children1(self):
        '''
        test count_children in tet without children
        '''
        username = 'u:1234'
        test_objekt = tet.TET(root=username)
        self.assertEqual(test_objekt.count_children(), {})

    def test_tet_count_children2(self):
        '''
        test count_children in tet with children
        '''
        username = 'u:1234'
        children = [tet.TETChild('high', children=tet.TETChild('action'))]
        test_objekt = tet.TET(root=username, children=children)
        self.assertEqual(test_objekt.count_children(), {'[high,[[action]]]': 1})

    def test_tet_count_children3(self):
        '''
        test count_children in tet with children
        '''
        username = 'u:1234'
        children = [tet.TETChild('high', children=tet.TETChild('action')),
                    tet.TETChild('high', children=tet.TETChild('action'))]
        test_objekt = tet.TET(root=username, children=children)
        self.assertEqual(test_objekt.count_children(), {'[high,[[action]]]': 2})

    def test_tet_count_children4(self):
        '''
        test count_children in tet with children
        '''
        username = 'u:1234'
        children = [tet.TETChild('high', children=tet.TETChild('action')),
                    tet.TETChild('low', children=tet.TETChild('action'))]
        test_objekt = tet.TET(root=username, children=children)
        self.assertEqual(test_objekt.count_children(),
                         {'[high,[[action]]]': 1, '[low,[[action]]]': 1})

    def test_tet_find_most_with_rating1(self):
        '''
        test find_most_with_rating in tet
        '''
        username = 'u:1234'
        children = [tet.TETChild('high', children=tet.TETChild('action')),
                    tet.TETChild('low', children=tet.TETChild('action'))]
        test_objekt = tet.TET(root=username, children=children)
        self.assertEqual(test_objekt.find_most_with_rating('high'), [['[high,[[action]]]', 1]])

    def test_tet_find_most_with_rating2(self):
        '''
        test find_most_with_rating in tet
        '''
        username = 'u:1234'
        children = [tet.TETChild('high', children=tet.TETChild('action')),
                    tet.TETChild('low', children=tet.TETChild('action')),
                    tet.TETChild('high', children=tet.TETChild('action'))]
        test_objekt = tet.TET(root=username, children=children)
        self.assertEqual(test_objekt.find_most_with_rating('high'), [['[high,[[action]]]', 2]])

    def test_tet_find_most_with_rating3(self):
        '''
        test find_most_with_rating in tet
        '''
        username = 'u:1234'
        children = [tet.TETChild('high', children=tet.TETChild('action')),
                    tet.TETChild('low', children=tet.TETChild('action')),
                    tet.TETChild('high', children=tet.TETChild('action'))]
        test_objekt = tet.TET(root=username, children=children)
        self.assertEqual(test_objekt.find_most_with_rating('low'), [['[low,[[action]]]', 1]])

    def test_tet_find_most_with_rating4(self):
        '''
        test find_most_with_rating in tet
        '''
        username = 'u:1234'
        children = [tet.TETChild('high', children=tet.TETChild('action')),
                    tet.TETChild('high', children=tet.TETChild('comedy'))]
        test_objekt = tet.TET(root=username, children=children)
        self.assertEqual(test_objekt.find_most_with_rating('high'),
                         [['[high,[[action]]]', 1], ['[high,[[comedy]]]', 1]])

    def test_tet_find_most_with_rating5(self):
        '''
        test find_most_with_rating in tet
        '''
        username = 'u:1234'
        children = [tet.TETChild('low', children=tet.TETChild('action')),
                    tet.TETChild('low', children=tet.TETChild('comedy'))]
        test_objekt = tet.TET(root=username, children=children)
        self.assertEqual(test_objekt.find_most_with_rating('high'), [['[high,[[nohigh]]]', 0]])

class TestTETchild(unittest.TestCase):
    '''
    tests for the tetchild class
    '''
    def test_tetchild_construction1(self):
        '''
        test the construction of a tetchild
        '''
        test_objekt = tet.TETChild('action')
        self.assertIsInstance(test_objekt, tet.TETChild)
        self.assertIsInstance(test_objekt, tet.TET)

    def test_tetchild_construction2(self):
        '''
        test the construction of a tetchild
        '''
        children = [tet.TETChild('action')]
        test_objekt = tet.TETChild('high', children=children)
        self.assertEqual(test_objekt.getchildren(), children)

    def test_tetchild_construction3(self):
        '''
        test the construction of a tetchild
        '''
        children = [tet.TETChild('action')]
        test_objekt = tet.TETChild('high', children=children[0])
        self.assertEqual(test_objekt.getchildren(), children)

    def test_tetchild_tostring1(self):
        '''
        test tostring in tetchild
        '''
        test_objekt = tet.TETChild('action')
        self.assertEqual(test_objekt.tostring(), '[action]')

    def test_tetchild_tostring2(self):
        '''
        test tostring in tetchild
        '''
        children = [tet.TETChild('action')]
        test_objekt = tet.TETChild('high', children=children)
        self.assertEqual(test_objekt.tostring(), '[high,[[action]]]')

    def test_tetchild_tostring3(self):
        '''
        test tostring in tetchild
        '''
        children = [tet.TETChild('action'), tet.TETChild('comedy')]
        test_objekt = tet.TETChild('high', children=children)
        self.assertEqual(test_objekt.tostring(), '[high,[[action],[comedy]]]')

class Testbuild_tet(unittest.TestCase):
    '''
    tests for the build_tet.py
    '''
    def test_moviedict(self):
        '''
        tests the construction of a movie dictionary
        '''
        test_dict = build_tet.moviedict(Paths.MOVIE_NODES_PATH)
        for thing in test_dict:
            self.assertEqual(len(test_dict[thing]), 4)
            self.assertIsInstance(test_dict[thing][0], str)
            self.assertIsInstance(test_dict[thing][1], str)
            self.assertIsInstance(test_dict[thing][2], str)
            self.assertIsInstance(test_dict[thing][3], list)
            self.assertIsInstance(test_dict[thing][3][0], str)

    def test_userdict(self):
        '''
        tests the construction of a user dictionary
        '''
        test_dict = build_tet.userdict(Paths.USER_NODES_PATH)
        for thing in test_dict:
            self.assertIsInstance(test_dict[thing], bool)

    def test_tet_find_tree1(self):
        '''
        tests the find_tree where the tet exists
        '''
        username = 'u:1234'
        children = [tet.TETChild('high', children=tet.TETChild('action')),
                    tet.TETChild('high', children=tet.TETChild('action'))]
        test_tet = tet.TET(root=username, children=children)
        test_tets = {username:test_tet}
        self.assertEqual(build_tet.tet_find_tree(username, test_tets), test_tet)

    def test_tet_find_tree2(self):
        '''
        tests the find_tree where the tet does not exists
        '''
        username = 'u:1234'
        children = [tet.TETChild('high', children=tet.TETChild('action')),
                    tet.TETChild('high', children=tet.TETChild('action'))]
        test_tet = tet.TET(root=username, children=children)
        test_tets = {username:test_tet}
        self.assertNotEqual(build_tet.tet_find_tree('u:5678', test_tets), test_tet)

    def test_construct_child1(self):
        '''
        tests the construct_child high rating
        '''
        movieid = 'm:1234'
        rating = '4.3'
        movie = ['1234', 'Toy Story (1995)',
                 '1995', ['Adventure', 'Animation', 'Children', 'Comedy', 'Fantasy']]
        dictofmovies = {'m:1234': movie}
        test_child = build_tet.construct_child(movieid, rating, dictofmovies)
        self.assertEqual(test_child.getroot(), 'high')

    def test_construct_child2(self):
        '''
        tests the construct_child mid rating
        '''
        movieid = 'm:1234'
        rating = '3.0'
        movie = ['1234', 'Toy Story (1995)',
                 '1995', ['Adventure', 'Animation', 'Children', 'Comedy', 'Fantasy']]
        dictofmovies = {'m:1234': movie}
        test_child = build_tet.construct_child(movieid, rating, dictofmovies)
        self.assertEqual(test_child.getroot(), 'mid')

    def test_construct_child3(self):
        '''
        tests the construct_child low rating
        '''
        movieid = 'm:1234'
        rating = '2.3'
        movie = ['1234', 'Toy Story (1995)',
                 '1995', ['Adventure', 'Animation', 'Children', 'Comedy', 'Fantasy']]
        dictofmovies = {'m:1234': movie}
        test_child = build_tet.construct_child(movieid, rating, dictofmovies)
        self.assertEqual(test_child.getroot(), 'low')

    def test_build_tets(self):
        '''
        tests the constructions of TETs
        '''
        edges = ['M:1234,U:1,5.0\n',
                 'M:5678,U:1,3.5\n',
                 'M:1234,U:2,2.0\n',
                 'M:5678,U:2,3.0\n',
                 'M:1234,U:3,3.5\n',
                 'M:5678,U:3,4.0\n']
        moviedict = {'M:1234': ['1234', 'Toy Story (1995)', '1995',
                                ['Adventure', 'Animation', 'Children', 'Comedy', 'Fantasy']],
                     'M:5678': ['5678', 'Jumanji (1995)', '1995',
                                ['Adventure', 'Children', 'Fantasy']]}
        test_tets = build_tet.build_tets(edges, moviedict, Paths.USER_NODES_PATH)
        self.assertEqual(len(test_tets), 3)
        for tetid in test_tets:
            self.assertIsInstance(test_tets[tetid], tet.TET)

    def test_save_load_tets(self):
        '''
        tests if safe and load does construct equivalent trees
        '''
        tets_path = pathlib.Path.cwd() / 'TET_test_save.csv'
        edges = ['M:1234,U:1,5.0\n',
                 'M:5678,U:1,3.5\n',
                 'M:3456,U:2,2.0\n',
                 'M:5678,U:2,1.0\n',
                 'M:1234,U:3,3.5\n',
                 'M:5678,U:3,4.0\n']
        moviedict = {'M:1234': ['1234', 'Toy Story (1995)', '1995',
                                ['Adventure', 'Animation', 'Children', 'Comedy', 'Fantasy']],
                     'M:5678': ['5678', 'Jumanji (1995)', '1995',
                                ['Adventure', 'Children', 'Fantasy']],
                     'M:3456': ['3456', 'Jumanji (1995)', '1995',
                                ['Adventure', 'Children', 'Fantasy']]}
        test_tets = build_tet.build_tets(edges, moviedict, Paths.USER_NODES_PATH)
        build_tet.save_tets(test_tets, tets_path)
        load_tets = build_tet.load_tets(tets_path)
        for ktet in test_tets:
            tet1 = test_tets[ktet]
            tet2 = load_tets[ktet]
            self.assertEqual(tet1.getroot(), tet2.getroot())
            self.assertEqual(len(tet1.getchildren()), len(tet2.getchildren()))
            self.assertEqual(tet1.tostring(), tet2.tostring())

    def test_grouping(self):
        '''
        tests grouping by tets of users
        '''
        edges = ['M:1234,U:1,5.0\n',
                 'M:5678,U:1,3.5\n',
                 'M:3456,U:2,2.0\n',
                 'M:5678,U:2,1.0\n',
                 'M:1234,U:3,3.5\n',
                 'M:5678,U:3,4.0\n']
        moviedict = {'M:1234': ['1234', 'Toy Story (1995)', '1995',
                                ['Adventure', 'Animation', 'Children', 'Comedy', 'Fantasy']],
                     'M:5678': ['5678', 'Jumanji (1995)', '1995',
                                ['Adventure', 'Children', 'Fantasy']],
                     'M:3456': ['3456', 'Jumanji (1995)', '1995',
                                ['Adventure', 'Children', 'Fantasy']]}
        test_tets = build_tet.build_tets(edges, moviedict, Paths.USER_NODES_PATH)
        groups = build_tet.grouping(test_tets)

        for group in groups:
            self.assertIn(group, ['Adventure', 'Animation', 'Children',
                                  'Comedy', 'Fantasy', 'nohigh'])

        self.assertEqual(len(groups['Adventure']), 2)
        self.assertEqual(len(groups['nohigh']), 1)

class testcompare_tet(unittest.TestCase):
    '''
    tests for the compare_tet.py
    '''
    def test_find_all_keys_in_dicts(self):
        '''
        tests find_all_keys_in_dicts combintng two list
        '''
        dict1 = {'key1':1,
                 'key2':2}
        dict2 = {'key2':3,
                 'key3':4}
        test_list = compare_tet.find_all_keys_in_dicts(list(dict1), list(dict2))
        self.assertEqual(test_list, ['key1', 'key2', 'key3'])

    def test_manhatten_distance1(self):
        '''
        tests manhatten_distance on the same tet
        '''
        edges = ['M:1234,U:1,5.0\n',
                 'M:5678,U:1,3.5\n',
                 'M:3456,U:2,2.0\n',
                 'M:5678,U:2,1.0\n',
                 'M:1234,U:3,3.5\n',
                 'M:5678,U:3,4.0\n']
        moviedict = {'M:1234': ['1234', 'Toy Story (1995)', '1995',
                                ['Adventure', 'Animation', 'Children', 'Comedy', 'Fantasy']],
                     'M:5678': ['5678', 'Jumanji (1995)', '1995',
                                ['Adventure', 'Children', 'Fantasy']],
                     'M:3456': ['3456', 'Jumanji (1995)', '1995',
                                ['Adventure', 'Children', 'Fantasy']]}
        test_tets = build_tet.build_tets(edges, moviedict, Paths.USER_NODES_PATH)
        self.assertEqual(compare_tet.manhatten_distance(test_tets['U:1'], test_tets['U:1']), 0)

    def test_manhatten_distance2(self):
        '''
        tests manhatten_distance on most distant tets
        '''
        edges = ['M:1234,U:1,5.0\n',
                 'M:5678,U:1,3.5\n',
                 'M:3456,U:2,2.0\n',
                 'M:5678,U:2,1.0\n',
                 'M:1234,U:3,3.5\n',
                 'M:5678,U:3,4.0\n']
        moviedict = {'M:1234': ['1234', 'Toy Story (1995)', '1995',
                                ['Adventure', 'Animation', 'Children', 'Comedy', 'Fantasy']],
                     'M:5678': ['5678', 'Jumanji (1995)', '1995',
                                ['Adventure', 'Children', 'Fantasy']],
                     'M:3456': ['3456', 'Jumanji (1995)', '1995',
                                ['Adventure', 'Children', 'Fantasy']]}
        test_tets = build_tet.build_tets(edges, moviedict, Paths.USER_NODES_PATH)
        self.assertEqual(compare_tet.manhatten_distance(test_tets['U:1'], test_tets['U:2']), 2)

    def test_manhatten_distance3(self):
        '''
        tests manhatten_distance on tets that have somthing in common
        '''
        edges = ['M:1234,U:1,5.0\n',
                 'M:5678,U:1,3.5\n',
                 'M:3456,U:2,2.0\n',
                 'M:5678,U:2,1.0\n',
                 'M:1234,U:3,4.5\n',
                 'M:5678,U:3,4.0\n']
        moviedict = {'M:1234': ['1234', 'Toy Story (1995)', '1995',
                                ['Adventure', 'Animation', 'Children', 'Comedy', 'Fantasy']],
                     'M:5678': ['5678', 'Jumanji (1995)', '1995',
                                ['Adventure', 'Children', 'Fantasy']],
                     'M:3456': ['3456', 'Jumanji (1995)', '1995',
                                ['Adventure', 'Children', 'Fantasy']]}
        test_tets = build_tet.build_tets(edges, moviedict, Paths.USER_NODES_PATH)
        self.assertEqual(compare_tet.manhatten_distance(test_tets['U:1'], test_tets['U:3']), 1)

    def test_graph_edit_distance1(self):
        '''
        tests graph_edit_distance on the same tet
        '''
        edges = ['M:1234,U:1,5.0\n',
                 'M:5678,U:1,3.5\n',
                 'M:3456,U:2,2.0\n',
                 'M:5678,U:2,1.0\n',
                 'M:1234,U:3,4.5\n',
                 'M:5678,U:3,4.0\n']
        moviedict = {'M:1234': ['1234', 'Toy Story (1995)', '1995',
                                ['Adventure', 'Animation', 'Children', 'Comedy', 'Fantasy']],
                     'M:5678': ['5678', 'Jumanji (1995)', '1995',
                                ['Adventure', 'Children', 'Fantasy']],
                     'M:3456': ['3456', 'Jumanji (1995)', '1995',
                                ['Adventure', 'Children', 'Fantasy']]}
        test_tets = build_tet.build_tets(edges, moviedict, Paths.USER_NODES_PATH)
        self.assertEqual(compare_tet.graph_edit_distance(test_tets['U:1'], test_tets['U:1']), 0)

    def test_graph_edit_distance2(self):
        '''
        tests graph_edit_distance on most distant tets
        '''
        edges = ['M:1234,U:1,5.0\n',
                 'M:5678,U:1,3.5\n',
                 'M:3456,U:2,2.0\n',
                 'M:5678,U:2,1.0\n',
                 'M:1234,U:3,4.5\n',
                 'M:5678,U:3,4.0\n']
        moviedict = {'M:1234': ['1234', 'Toy Story (1995)', '1995',
                                ['Adventure', 'Animation', 'Children', 'Comedy', 'Fantasy']],
                     'M:5678': ['5678', 'Jumanji (1995)', '1995',
                                ['Adventure', 'Children', 'Fantasy']],
                     'M:3456': ['3456', 'Jumanji (1995)', '1995',
                                ['Adventure', 'Children', 'Fantasy']]}
        test_tets = build_tet.build_tets(edges, moviedict, Paths.USER_NODES_PATH)
        self.assertEqual(compare_tet.graph_edit_distance(test_tets['U:1'], test_tets['U:2']), 2)

    def test_graph_edit_distance3(self):
        '''
        tests graph_edit_distance on tets that have somthing in common
        '''
        edges = ['M:1234,U:1,5.0\n',
                 'M:5678,U:1,3.5\n',
                 'M:3456,U:2,2.0\n',
                 'M:5678,U:2,1.0\n',
                 'M:1234,U:3,4.5\n',
                 'M:5678,U:3,4.0\n']
        moviedict = {'M:1234': ['1234', 'Toy Story (1995)', '1995',
                                ['Adventure', 'Animation', 'Children', 'Comedy', 'Fantasy']],
                     'M:5678': ['5678', 'Jumanji (1995)', '1995',
                                ['Adventure', 'Children', 'Fantasy']],
                     'M:3456': ['3456', 'Jumanji (1995)', '1995',
                                ['Adventure', 'Children', 'Fantasy']]}
        test_tets = build_tet.build_tets(edges, moviedict, Paths.USER_NODES_PATH)
        self.assertEqual(compare_tet.graph_edit_distance(test_tets['U:1'], test_tets['U:3']), 1.5)

    def test_cost(self):
        '''
        test cost function
        '''
        self.assertEqual(compare_tet.cost('low'), 0.25)
        self.assertEqual(compare_tet.cost('mid'), 0.5)
        self.assertEqual(compare_tet.cost('high'), 1)

    def test_knn1(self):
        '''
        test knn
        '''
        edges = ['M:1234,U:1,5.0\n',
                 'M:5678,U:1,3.5\n',
                 'M:3456,U:2,2.0\n',
                 'M:5678,U:2,1.0\n',
                 'M:1234,U:3,4.5\n',
                 'M:5678,U:3,4.0\n']
        moviedict = {'M:1234': ['1234', 'Toy Story (1995)', '1995',
                                ['Adventure', 'Animation', 'Children', 'Comedy', 'Fantasy']],
                     'M:5678': ['5678', 'Jumanji (1995)', '1995',
                                ['Adventure', 'Children', 'Fantasy']],
                     'M:3456': ['3456', 'Jumanji (1995)', '1995',
                                ['Adventure', 'Children', 'Fantasy']]}
        userdatabase = {'U:1': {'M:1234': 5.0, 'M:5678': 3.5},
                        'U:2': {'M:3456': 2.0, 'M:5678': 1.0},
                        'U:3': {'M:1234': 4.5, 'M:5678': 4.0}}
        test_tets = build_tet.build_tets(edges, moviedict, Paths.USER_NODES_PATH)

        preds = compare_tet.knn(test_tets['U:1'], list(test_tets.values()),
                                user_database=userdatabase)
        self.assertEqual(preds, [('M:3456', 4.75)])

    def test_knn2(self):
        '''
        test knn standard filter
        '''
        edges = ['M:1234,U:1,5.0\n',
                 'M:5678,U:1,3.5\n',
                 'M:3456,U:2,2.0\n',
                 'M:5678,U:2,1.0\n',
                 'M:1234,U:3,4.5\n',
                 'M:5678,U:3,4.0\n']
        moviedict = {'M:1234': ['1234', 'Toy Story (1995)', '1995',
                                ['Adventure', 'Animation', 'Children', 'Comedy', 'Fantasy']],
                     'M:5678': ['5678', 'Jumanji (1995)', '1995',
                                ['Adventure', 'Children', 'Fantasy']],
                     'M:3456': ['3456', 'Jumanji (1995)', '1995',
                                ['Adventure', 'Children', 'Fantasy']]}
        userdatabase = {'U:1': {'M:1234': 4.25},
                        'U:2': {'M:3456': 2.0, 'M:5678': 1.0},
                        'U:3': {'M:1234': 4.5, 'M:5678': 4.0}}
        test_tets = build_tet.build_tets(edges, moviedict, Paths.USER_NODES_PATH)
        preds = compare_tet.knn(test_tets['U:1'], list(test_tets.values()),
                                user_database=userdatabase)
        self.assertEqual(preds, [('M:3456', 4.75)])

    def test_knn3(self):
        '''
        test knn lowered filter
        '''
        edges = ['M:1234,U:1,5.0\n',
                 'M:5678,U:1,3.5\n',
                 'M:3456,U:2,2.0\n',
                 'M:5678,U:2,1.0\n',
                 'M:1234,U:3,4.5\n',
                 'M:5678,U:3,4.0\n']
        moviedict = {'M:1234': ['1234', 'Toy Story (1995)', '1995',
                                ['Adventure', 'Animation', 'Children', 'Comedy', 'Fantasy']],
                     'M:5678': ['5678', 'Jumanji (1995)', '1995',
                                ['Adventure', 'Children', 'Fantasy']],
                     'M:3456': ['3456', 'Jumanji (1995)', '1995',
                                ['Adventure', 'Children', 'Fantasy']]}
        userdatabase = {'U:1': {'M:1234': 4.25},
                        'U:2': {'M:3456': 2.0, 'M:5678': 1.0},
                        'U:3': {'M:1234': 4.5, 'M:5678': 4.0}}
        test_tets = build_tet.build_tets(edges, moviedict, Paths.USER_NODES_PATH)
        preds = compare_tet.knn(test_tets['U:1'], list(test_tets.values()),
                                user_database=userdatabase, filterv=3)
        self.assertEqual(preds, [('M:5678', 3.8928571428571423), ('M:3456', 4.75)])


    def test_pred1(self):
        '''
        test pred one film not seen by user no filter
        '''
        edges = ['M:1234,U:1,5.0\n',
                 'M:5678,U:1,3.5\n',
                 'M:3456,U:2,2.0\n',
                 'M:5678,U:2,1.0\n',
                 'M:1234,U:3,4.5\n',
                 'M:5678,U:3,4.0\n']
        moviedict = {'M:1234': ['1234', 'Toy Story (1995)', '1995',
                                ['Adventure', 'Animation', 'Children', 'Comedy', 'Fantasy']],
                     'M:5678': ['5678', 'Jumanji (1995)', '1995',
                                ['Adventure', 'Children', 'Fantasy']],
                     'M:3456': ['3456', 'Jumanji (1995)', '1995',
                                ['Adventure', 'Children', 'Fantasy']]}
        userdatabase = {'U:1': {'M:1234': 5.0, 'M:5678': 3.5},
                        'U:2': {'M:3456': 2.0, 'M:5678': 1.0},
                        'U:3': {'M:1234': 4.5, 'M:5678': 4.0}}
        test_tets = build_tet.build_tets(edges, moviedict, Paths.USER_NODES_PATH)
        best = [[test_tets['U:2'], 54], [test_tets['U:3'], 67]]
        self.assertEqual(compare_tet.pred(test_tets['U:1'], best, userdatabase), [('M:3456', 4.75)])

    def test_pred2(self):
        '''
        test pred two film not seen by user no filter
        '''
        edges = ['M:1234,U:1,5.0\n',
                 'M:5678,U:1,3.5\n',
                 'M:3456,U:2,2.0\n',
                 'M:5678,U:2,1.0\n',
                 'M:1234,U:3,4.5\n',
                 'M:5678,U:3,4.0\n']
        moviedict = {'M:1234': ['1234', 'Toy Story (1995)', '1995',
                                ['Adventure', 'Animation', 'Children', 'Comedy', 'Fantasy']],
                     'M:5678': ['5678', 'Jumanji (1995)', '1995',
                                ['Adventure', 'Children', 'Fantasy']],
                     'M:3456': ['3456', 'Jumanji (1995)', '1995',
                                ['Adventure', 'Children', 'Fantasy']]}
        userdatabase = {'U:1': {'M:1234': 4.25},
                        'U:2': {'M:3456': 2.0, 'M:5678': 1.0},
                        'U:3': {'M:1234': 4.5, 'M:5678': 4.0}}
        test_tets = build_tet.build_tets(edges, moviedict, Paths.USER_NODES_PATH)
        best = [[test_tets['U:2'], 54], [test_tets['U:3'], 67]]
        self.assertEqual(compare_tet.pred(test_tets['U:1'], best, userdatabase),
                         [('M:3456', 4.75), ('M:5678', 3.861570247933884)])

    def test_pred3(self):
        '''
        test pred two film not seen by user filter 4
        '''
        edges = ['M:1234,U:1,5.0\n',
                 'M:5678,U:1,3.5\n',
                 'M:3456,U:2,2.0\n',
                 'M:5678,U:2,1.0\n',
                 'M:1234,U:3,4.5\n',
                 'M:5678,U:3,4.0\n']
        moviedict = {'M:1234': ['1234', 'Toy Story (1995)', '1995',
                                ['Adventure', 'Animation', 'Children', 'Comedy', 'Fantasy']],
                     'M:5678': ['5678', 'Jumanji (1995)', '1995',
                                ['Adventure', 'Children', 'Fantasy']],
                     'M:3456': ['3456', 'Jumanji (1995)', '1995',
                                ['Adventure', 'Children', 'Fantasy']]}
        userdatabase = {'U:1': {'M:1234': 4.25},
                        'U:2': {'M:3456': 2.0, 'M:5678': 1.0},
                        'U:3': {'M:1234': 4.5, 'M:5678': 4.0}}
        test_tets = build_tet.build_tets(edges, moviedict, Paths.USER_NODES_PATH)
        best = [[test_tets['U:2'], 54], [test_tets['U:3'], 67]]
        self.assertEqual(compare_tet.pred(test_tets['U:1'], best, userdatabase, 4),
                         [('M:3456', 4.75)])

    def test_reasing_sims1(self):
        '''
        test reasing_sims on uneven number of items in list
        '''
        sims = [['sam', 10],
                ['ams', 5],
                ['bob', 1]]
        res = [['sam', 1],
               ['ams', 5],
               ['bob', 10]]
        self.assertEqual(compare_tet.reasing_sims(sims), res)

    def test_reasing_sims2(self):
        '''
        test reasing_sims on even number of items in list
        '''
        sims = [['sam', 10],
                ['ams', 5],
                ['msa', 3],
                ['bob', 1]]
        res = [['sam', 1],
               ['ams', 3],
               ['msa', 5],
               ['bob', 10]]
        self.assertEqual(compare_tet.reasing_sims(sims), res)

    '''
    this can not run on git because of the missing graph.csv file
    def test_userdatabase(self):
        '''
        #test userdatabase and values
    '''
        test_userdatabase = compare_tet.userdatabase()
        for user in test_userdatabase:
            self.assertIn('U', user)
            for movie in test_userdatabase[user]:
                self.assertIn('M', movie)
                self.assertIsInstance(test_userdatabase[user][movie], float)
    '''

if __name__ == "__main__":
    unittest.main()
