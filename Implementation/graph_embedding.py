from node2vec import Node2Vec
import networkx

graph = networkx.Graph()


# Generate walks
node2vec = Node2Vec(graph, dimensions=20, walk_length=16, num_walks=100)

# Learn embeddings 
model = node2vec.fit(window=10, min_count=1)