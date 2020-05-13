# Memory usage of the 25000000 ratings dataset
#### Reading the whole graph into networkx in Python 3.7:
About 10 - 15 GB.
## Reading the graph into an object with two lists nodes and edges in Python 3.7:
#### As observed through htop:
2.35 GB.
#### As calculated by psutil:
2.8 GB.
#### As calculated by sys.getsizeof() on the list of nodes and edges:
2.4 GB.
## Reading the graph into an object with two arrays nodes and edges in C++:
0.299 GB or 299 MB.  

# Memory usage of preprocess_transition_probs from nod2vec in python:
## Data:
* Nodes: 221588
* Edges: 25000095
* Average number of neighbors for a node: 225.64484538873947

With the size of float equal to 8 bytes, the function will use 180,7984008 GB of memory. This is even one of the lowest estimates, since we set the size of float to be equal to 8 bytes. For floats with size 24 bytes, the function will use 542 GB of memory.
