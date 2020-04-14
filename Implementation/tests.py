# The tests can both be run with python and pytest.
import unittest
import os
import Discretizedata
import TET
import build_tet
import pathlib
import compare_tet

# The test class for graph methods.
'''class TestDiscretizedata(unittest.TestCase):
    """ This class contains tests for the functions in Discretizedata.py."""
    RATING_DATA = [
        "userId,movieId,rating,timestamp",
        "1,296,5.0,1147880044",
        "1,306,3.5,1147868817",
        "1,307,5.0,1147868828",
        "1,665,5.0,1147878820",
    ]

    with open(Discretizedata.RATINGPATH, 'w') as writer:
        for line in RATING_DATA:
            writer.write(line + os.linesep)

    def test_disc_rating_data(self):
        """ Tests the disc_rating_data() function by using the first 5 lines
         in the ratings.csv file"""
        expected_value = [
            "296,1,5.0\n",
            "306,1,3.5\n",
            "307,1,5.0\n",
            "665,1,5.0\n"
        ]


        Discretizedata.disc_rating_data()
        with open(Discretizedata.GRAPH_DATA_PATH, 'r') as reader:
            graph_data = reader.readlines()
        self.assertEqual(graph_data[1:], expected_value)'''

class TestTET(unittest.TestCase):
    def test_Tet_construction(self):
        test_objekt = TET.TET()
        self.assertIsInstance(test_objekt, TET.TET)
    
    def test_Tet_getroot(self):
        username ='u:1234'
        test_objekt = TET.TET(root=username)
        self.assertIs(test_objekt.getroot(), username)
    
    def test_Tet_isroot(self):
        username ='u:1234'
        test_objekt = TET.TET(root=username)
        self.assertTrue(test_objekt.isroot(username))

    def test_tet_getchildren(self):
        username ='u:1234'
        children = [TET.TETChild('Lars')]
        test_objekt = TET.TET(root=username, children=children)
        self.assertEqual(test_objekt.getchildren(), children)
    
    def test_tet_tostring1(self):
        username ='u:1234'
        test_objekt = TET.TET(root=username)
        self.assertEqual(test_objekt.tostring(), '[u:1234]')
    
    def test_tet_tostring2(self):
        username ='u:1234'
        children = [TET.TETChild('high', children=TET.TETChild('action'))]
        test_objekt = TET.TET(root=username, children=children)
        self.assertEqual(test_objekt.tostring(), '[u:1234,[[high,[[action]]]:1]]')
   
    def test_tet_tostring3(self):
        username ='u:1234'
        children = [TET.TETChild('high', children=TET.TETChild('action')), TET.TETChild('high', children=TET.TETChild('action'))]
        test_objekt = TET.TET(root=username, children=children)
        self.assertEqual(test_objekt.tostring(), '[u:1234,[[high,[[action]]]:2]]')

    def test_tet_tostring4(self):
        username ='u:1234'
        children = [TET.TETChild('high', children=TET.TETChild('action')), TET.TETChild('low', children=TET.TETChild('action'))]
        test_objekt = TET.TET(root=username, children=children)
        self.assertEqual(test_objekt.tostring(), '[u:1234,[[high,[[action]]]:1,[low,[[action]]]:1]]')

    def test_tet_count_children1(self):
        username ='u:1234'
        test_objekt = TET.TET(root=username)
        self.assertEqual(test_objekt.count_children(), {})

    def test_tet_count_children2(self):
        username ='u:1234'
        children = [TET.TETChild('high', children=TET.TETChild('action'))]
        test_objekt = TET.TET(root=username, children=children)
        self.assertEqual(test_objekt.count_children(), {'[high,[[action]]]': 1})

    def test_tet_count_children3(self):
        username ='u:1234'
        children = [TET.TETChild('high', children=TET.TETChild('action')), TET.TETChild('high', children=TET.TETChild('action'))]
        test_objekt = TET.TET(root=username, children=children)
        self.assertEqual(test_objekt.count_children(), {'[high,[[action]]]': 2})

    def test_tet_count_children4(self):
        username ='u:1234'
        children = [TET.TETChild('high', children=TET.TETChild('action')), TET.TETChild('low', children=TET.TETChild('action'))]
        test_objekt = TET.TET(root=username, children=children)
        self.assertEqual(test_objekt.count_children(), {'[high,[[action]]]': 1, '[low,[[action]]]': 1})

    def test_tet_find_most_with_rating1(self):
        username ='u:1234'
        children = [TET.TETChild('high', children=TET.TETChild('action')), TET.TETChild('low', children=TET.TETChild('action'))]
        test_objekt = TET.TET(root=username, children=children)
        self.assertEqual(test_objekt.find_most_with_rating('high'), [['[high,[[action]]]', 1]])

    def test_tet_find_most_with_rating2(self):
        username ='u:1234'
        children = [TET.TETChild('high', children=TET.TETChild('action')), TET.TETChild('low', children=TET.TETChild('action')), TET.TETChild('high', children=TET.TETChild('action'))]
        test_objekt = TET.TET(root=username, children=children)
        self.assertEqual(test_objekt.find_most_with_rating('high'), [['[high,[[action]]]', 2]])

    def test_tet_find_most_with_rating3(self):
        username ='u:1234'
        children = [TET.TETChild('high', children=TET.TETChild('action')), TET.TETChild('low', children=TET.TETChild('action')), TET.TETChild('high', children=TET.TETChild('action'))]
        test_objekt = TET.TET(root=username, children=children)
        self.assertEqual(test_objekt.find_most_with_rating('low'), [['[low,[[action]]]', 1]])

    def test_tet_find_most_with_rating4(self):
        username ='u:1234'
        children = [TET.TETChild('high', children=TET.TETChild('action')), TET.TETChild('high', children=TET.TETChild('comedy'))]
        test_objekt = TET.TET(root=username, children=children)
        self.assertEqual(test_objekt.find_most_with_rating('high'), [['[high,[[action]]]', 1],['[high,[[comedy]]]', 1]])

    def test_tet_find_most_with_rating5(self):
        username ='u:1234'
        children = [TET.TETChild('low', children=TET.TETChild('action')), TET.TETChild('low', children=TET.TETChild('comedy'))]
        test_objekt = TET.TET(root=username, children=children)
        self.assertEqual(test_objekt.find_most_with_rating('high'), [['[high,[[nohigh]]]', 0]])

class TestTETchild(unittest.TestCase):
    def test_TetChild_construction1(self):
        test_objekt = TET.TETChild('action')
        self.assertIsInstance(test_objekt, TET.TETChild)
        self.assertIsInstance(test_objekt, TET.TET)
    
    def test_TetChild_construction2(self):
        children = [TET.TETChild('action')]
        test_objekt = TET.TETChild('high', children=children)
        self.assertEqual(test_objekt.getchildren(), children)
    
    def test_TetChild_construction3(self):
        children = [TET.TETChild('action')]
        test_objekt = TET.TETChild('high', children=children[0])
        self.assertEqual(test_objekt.getchildren(), children)

    def test_tetchild_tostring1(self):
        test_objekt = TET.TETChild('action')
        self.assertEqual(test_objekt.tostring(), '[action]')

    def test_tetchild_tostring2(self):
        children = [TET.TETChild('action')]
        test_objekt = TET.TETChild('high', children=children)
        self.assertEqual(test_objekt.tostring(), '[high,[[action]]]')

    def test_tetchild_tostring3(self):
        children = [TET.TETChild('action'),TET.TETChild('comedy')]
        test_objekt = TET.TETChild('high', children=children)
        self.assertEqual(test_objekt.tostring(), '[high,[[action],[comedy]]]')

class Testbuild_tet(unittest.TestCase):
    def test_moviedict(self):
        MOVIE_NODES_PATH = pathlib.Path.cwd() / 'Movielens_data' / 'movie_nodes.csv'
        test_dict = build_tet.moviedict(MOVIE_NODES_PATH)
        for thing in test_dict:
            self.assertEqual(len(test_dict[thing]), 4)
            self.assertIsInstance(test_dict[thing][0], str)
            self.assertIsInstance(test_dict[thing][1], str)
            self.assertIsInstance(test_dict[thing][2], str)
            self.assertIsInstance(test_dict[thing][3], list)
            self.assertIsInstance(test_dict[thing][3][0], str)
    
    def test_userdict(self):
        USER_NODES_PATH = pathlib.Path.cwd() / 'Movielens_data' / 'user_nodes.csv'
        test_dict = build_tet.userdict(USER_NODES_PATH)
        for thing in test_dict:
            self.assertIsInstance(test_dict[thing], bool)
    
    def test_tet_find_tree1(self):
        username ='u:1234'
        children = [TET.TETChild('high', children=TET.TETChild('action')), TET.TETChild('high', children=TET.TETChild('action'))]
        test_tet = TET.TET(root=username, children=children)
        test_tets = {username:test_tet}
        self.assertEqual(build_tet.tet_find_tree(username, test_tets), test_tet)
        
    def test_tet_find_tree2(self):
        username ='u:1234'
        children = [TET.TETChild('high', children=TET.TETChild('action')), TET.TETChild('high', children=TET.TETChild('action'))]
        test_tet = TET.TET(root=username, children=children)
        test_tets = {username:test_tet}
        self.assertNotEqual(build_tet.tet_find_tree('u:5678', test_tets), test_tet)

    def test_construct_child1(self):
        movieid='m:1234'
        rating = '4.3'
        movie = ['1234','Toy Story (1995)','1995',['Adventure','Animation','Children','Comedy','Fantasy']]
        dictofmovies = {'m:1234': movie}
        test_child = build_tet.construct_child(movieid,rating,dictofmovies)
        self.assertEqual(test_child.getroot(), 'high')
    
    def test_construct_child2(self):
        movieid='m:1234'
        rating = '3.0'
        movie = ['1234','Toy Story (1995)','1995',['Adventure','Animation','Children','Comedy','Fantasy']]
        dictofmovies = {'m:1234': movie}
        test_child = build_tet.construct_child(movieid,rating,dictofmovies)
        self.assertEqual(test_child.getroot(), 'mid')
    
    def test_construct_child3(self):
        movieid='m:1234'
        rating = '2.3'
        movie = ['1234','Toy Story (1995)','1995',['Adventure','Animation','Children','Comedy','Fantasy']]
        dictofmovies = {'m:1234': movie}
        test_child = build_tet.construct_child(movieid,rating,dictofmovies)
        self.assertEqual(test_child.getroot(), 'low')
    
    def test_build_tets(self):
        edges = ['M:1234,U:1,5.0\n',
                 'M:5678,U:1,3.5\n',
                 'M:1234,U:2,2.0\n',
                 'M:5678,U:2,3.0\n',
                 'M:1234,U:3,3.5\n',
                 'M:5678,U:3,4.0\n']
        moviedict = {'M:1234': ['1234','Toy Story (1995)','1995',['Adventure','Animation','Children','Comedy','Fantasy']],
                     'M:5678': ['5678','Jumanji (1995)','1995',['Adventure','Children','Fantasy']]}
        USER_NODES_PATH = pathlib.Path.cwd() / 'Movielens_data' / 'user_nodes.csv'
        test_tets = build_tet.build_tets(edges, moviedict, USER_NODES_PATH)
        self.assertEqual(len(test_tets),3)
        for tet in test_tets:
            self.assertIsInstance(test_tets[tet],TET.TET)

    def test_save_load_tets(self):
        TETS_PATH = pathlib.Path.cwd() / 'TET_test_save.csv'
        edges = ['M:1234,U:1,5.0\n',
                 'M:5678,U:1,3.5\n',
                 'M:3456,U:2,2.0\n',
                 'M:5678,U:2,1.0\n',
                 'M:1234,U:3,3.5\n',
                 'M:5678,U:3,4.0\n']
        moviedict = {'M:1234': ['1234','Toy Story (1995)','1995',['Adventure','Animation','Children','Comedy','Fantasy']],
                     'M:5678': ['5678','Jumanji (1995)','1995',['Adventure','Children','Fantasy']],
                     'M:3456': ['3456','Jumanji (1995)','1995',['Adventure','Children','Fantasy']]}
        USER_NODES_PATH = pathlib.Path.cwd() / 'Movielens_data' / 'user_nodes.csv'
        test_tets = build_tet.build_tets(edges, moviedict, USER_NODES_PATH)
        build_tet.save_tets(test_tets, TETS_PATH)
        load_tets = build_tet.load_tets(TETS_PATH)
        for tet in test_tets:
            tet1 = test_tets[tet]
            tet2 = load_tets[tet]
            self.assertEqual(tet1.getroot(), tet2.getroot())
            self.assertEqual(len(tet1.getchildren()), len(tet2.getchildren()))
            self.assertEqual(tet1.tostring(),tet2.tostring())
    
    def test_grouping(self):
        edges = ['M:1234,U:1,5.0\n',
                 'M:5678,U:1,3.5\n',
                 'M:3456,U:2,2.0\n',
                 'M:5678,U:2,1.0\n',
                 'M:1234,U:3,3.5\n',
                 'M:5678,U:3,4.0\n']
        moviedict = {'M:1234': ['1234','Toy Story (1995)','1995',['Adventure','Animation','Children','Comedy','Fantasy']],
                     'M:5678': ['5678','Jumanji (1995)','1995',['Adventure','Children','Fantasy']],
                     'M:3456': ['3456','Jumanji (1995)','1995',['Adventure','Children','Fantasy']]}
        USER_NODES_PATH = pathlib.Path.cwd() / 'Movielens_data' / 'user_nodes.csv'
        test_tets = build_tet.build_tets(edges, moviedict, USER_NODES_PATH)
        groups = build_tet.grouping(test_tets)

        for group in groups:
            self.assertIn(group, ['Adventure','Animation','Children','Comedy','Fantasy', 'nohigh'])
        
        self.assertEqual(len(groups['Adventure']),2)
        self.assertEqual(len(groups['nohigh']),1)

class test_compare_tet(unittest.TestCase):
    def test_find_all_keys_in_dicts(self):
        dict1 = {'key1':1,
                 'key2':2}
        dict2 = {'key2':3,
                 'key3':4}
        test_list = compare_tet.find_all_keys_in_dicts(list(dict1),list(dict2))
        self.assertEqual(test_list,['key1','key2','key3'])
    
    def test_manhatten_distance1(self):
        edges = ['M:1234,U:1,5.0\n',
                 'M:5678,U:1,3.5\n',
                 'M:3456,U:2,2.0\n',
                 'M:5678,U:2,1.0\n',
                 'M:1234,U:3,3.5\n',
                 'M:5678,U:3,4.0\n']
        moviedict = {'M:1234': ['1234','Toy Story (1995)','1995',['Adventure','Animation','Children','Comedy','Fantasy']],
                     'M:5678': ['5678','Jumanji (1995)','1995',['Adventure','Children','Fantasy']],
                     'M:3456': ['3456','Jumanji (1995)','1995',['Adventure','Children','Fantasy']]}
        USER_NODES_PATH = pathlib.Path.cwd() / 'Movielens_data' / 'user_nodes.csv'
        test_tets = build_tet.build_tets(edges, moviedict, USER_NODES_PATH)
        self.assertEqual(compare_tet.manhatten_distance(test_tets['U:1'],test_tets['U:1']),0)

    def test_manhatten_distance2(self):
        edges = ['M:1234,U:1,5.0\n',
                 'M:5678,U:1,3.5\n',
                 'M:3456,U:2,2.0\n',
                 'M:5678,U:2,1.0\n',
                 'M:1234,U:3,3.5\n',
                 'M:5678,U:3,4.0\n']
        moviedict = {'M:1234': ['1234','Toy Story (1995)','1995',['Adventure','Animation','Children','Comedy','Fantasy']],
                     'M:5678': ['5678','Jumanji (1995)','1995',['Adventure','Children','Fantasy']],
                     'M:3456': ['3456','Jumanji (1995)','1995',['Adventure','Children','Fantasy']]}
        USER_NODES_PATH = pathlib.Path.cwd() / 'Movielens_data' / 'user_nodes.csv'
        test_tets = build_tet.build_tets(edges, moviedict, USER_NODES_PATH)
        self.assertEqual(compare_tet.manhatten_distance(test_tets['U:1'],test_tets['U:2']),2)

    def test_manhatten_distance3(self):
        edges = ['M:1234,U:1,5.0\n',
                 'M:5678,U:1,3.5\n',
                 'M:3456,U:2,2.0\n',
                 'M:5678,U:2,1.0\n',
                 'M:1234,U:3,4.5\n',
                 'M:5678,U:3,4.0\n']
        moviedict = {'M:1234': ['1234','Toy Story (1995)','1995',['Adventure','Animation','Children','Comedy','Fantasy']],
                     'M:5678': ['5678','Jumanji (1995)','1995',['Adventure','Children','Fantasy']],
                     'M:3456': ['3456','Jumanji (1995)','1995',['Adventure','Children','Fantasy']]}
        USER_NODES_PATH = pathlib.Path.cwd() / 'Movielens_data' / 'user_nodes.csv'
        test_tets = build_tet.build_tets(edges, moviedict, USER_NODES_PATH)
        self.assertEqual(compare_tet.manhatten_distance(test_tets['U:1'],test_tets['U:3']),1)

    def test_graph_edit_distance1(self):
        edges = ['M:1234,U:1,5.0\n',
                 'M:5678,U:1,3.5\n',
                 'M:3456,U:2,2.0\n',
                 'M:5678,U:2,1.0\n',
                 'M:1234,U:3,4.5\n',
                 'M:5678,U:3,4.0\n']
        moviedict = {'M:1234': ['1234','Toy Story (1995)','1995',['Adventure','Animation','Children','Comedy','Fantasy']],
                     'M:5678': ['5678','Jumanji (1995)','1995',['Adventure','Children','Fantasy']],
                     'M:3456': ['3456','Jumanji (1995)','1995',['Adventure','Children','Fantasy']]}
        USER_NODES_PATH = pathlib.Path.cwd() / 'Movielens_data' / 'user_nodes.csv'
        test_tets = build_tet.build_tets(edges, moviedict, USER_NODES_PATH)
        self.assertEqual(compare_tet.graph_edit_distance(test_tets['U:1'],test_tets['U:1']),0)
    
    def test_graph_edit_distance2(self):
        edges = ['M:1234,U:1,5.0\n',
                 'M:5678,U:1,3.5\n',
                 'M:3456,U:2,2.0\n',
                 'M:5678,U:2,1.0\n',
                 'M:1234,U:3,4.5\n',
                 'M:5678,U:3,4.0\n']
        moviedict = {'M:1234': ['1234','Toy Story (1995)','1995',['Adventure','Animation','Children','Comedy','Fantasy']],
                     'M:5678': ['5678','Jumanji (1995)','1995',['Adventure','Children','Fantasy']],
                     'M:3456': ['3456','Jumanji (1995)','1995',['Adventure','Children','Fantasy']]}
        USER_NODES_PATH = pathlib.Path.cwd() / 'Movielens_data' / 'user_nodes.csv'
        test_tets = build_tet.build_tets(edges, moviedict, USER_NODES_PATH)
        self.assertEqual(compare_tet.graph_edit_distance(test_tets['U:1'],test_tets['U:2']),2)

    def test_graph_edit_distance3(self):
        edges = ['M:1234,U:1,5.0\n',
                 'M:5678,U:1,3.5\n',
                 'M:3456,U:2,2.0\n',
                 'M:5678,U:2,1.0\n',
                 'M:1234,U:3,4.5\n',
                 'M:5678,U:3,4.0\n']
        moviedict = {'M:1234': ['1234','Toy Story (1995)','1995',['Adventure','Animation','Children','Comedy','Fantasy']],
                     'M:5678': ['5678','Jumanji (1995)','1995',['Adventure','Children','Fantasy']],
                     'M:3456': ['3456','Jumanji (1995)','1995',['Adventure','Children','Fantasy']]}
        USER_NODES_PATH = pathlib.Path.cwd() / 'Movielens_data' / 'user_nodes.csv'
        test_tets = build_tet.build_tets(edges, moviedict, USER_NODES_PATH)
        self.assertEqual(compare_tet.graph_edit_distance(test_tets['U:1'],test_tets['U:3']),1.5)

    def test_cost(self):
        self.assertEqual(compare_tet.cost('low'), 0.25)
        self.assertEqual(compare_tet.cost('mid'), 0.5)
        self.assertEqual(compare_tet.cost('high'), 1)
    
    def test_knn(self):
        pass

    def test_pred(self):
        pass

    def test_reasing_sims1(self):
        sims = [['sam',10],
                ['ams',5],
                ['bob',1]]
        res = [['sam',1],
               ['ams',5],
               ['bob',10]]
        self.assertEqual(compare_tet.reasing_sims(sims),res)
    
    def test_reasing_sims2(self):
        sims = [['sam',10],
                ['ams',5],
                ['msa',3],
                ['bob',1]]
        res = [['sam',1],
               ['ams',3],
               ['msa',5],
               ['bob',10]]
        self.assertEqual(compare_tet.reasing_sims(sims),res)

    def test_userdatabase(self):
        test_userdatabase = compare_tet.userdatabase()
        for user in test_userdatabase:
            self.assertIn('U', user)
            for movie in test_userdatabase[user]:
                self.assertIn('M', movie)
                self.assertIsInstance(test_userdatabase[user][movie],float)


if __name__ == "__main__":
    unittest.main()
