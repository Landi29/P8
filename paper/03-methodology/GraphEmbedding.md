In (**A Comprehensive Survey of Graph Embedding: Problems, Techniques, and Application**) HongYun Cai et al. discuss about the different ways of doing graph embedding. They split these different embedding strategies into input and output embedding which has 4 categories each. 

For input we have:

*Homogeneous graphs* which is graphs where both nodes and edges belong to a single type respectively, and can be further categorized by either adding weights, directions or both. Graphs that have only directions and no weights the nodes should be closer to each other depending on how they relate to each other, so two nodes that are related should be similar.

*Heterogeneous graphs* can have nodes and edges of multiple types which is typically things like knowledge graphs where edges and nodes usually represent different relations and entities respectively. For example a knowledge graph over some film relations could have the entities "Director", "Actor" and "Film" where the relations would then be "Produce", "Direct" and "Act-in".

*Graph with Auxiliary Information* is any graph that contains extra information for a node or relation. To give an example of this we could have the category of nodes called "Book", which contains information about the book and its author. The node in this case would be the name of the book and author could be auxiliary information.

*Graph constructed from non-relational data* instead of providing the input graph we construct it from non-relational input data, this is usually done when the input data is assumed to be in a low dimensional manifold. In this kind of graph relations can be discovered by using methods like K-Nearest-Neighbours.

For output we have:

*Node embedding* is the act of taking the nodes in the graph and represent them as a vector. When doing this two nodes that were similar in the graph should have similar vectors and therefore be able to be identified.

*Edge Embedding* is a bit more complex. Given a relation between two nodes a triplet is created *<h,r,t>*  where h and t are the head and tail node and r is the relation using this it is possible to given two of the three components to predict what the last component should be.

*Hybrid Embedding* spans over a few different embedding methods like substructure embedding where each node and edges are embedding for a smaller section of the graph then combined. This can then be used to find substructures that are similar to each other.

*Whole-Graph Embedding* is the idea of representing the whole graph as one single vector and is therefore usually only done on small graphs like proteins and molecules. But this is also the hardest one to do as an embedding method wants to be reversible, but this method can forget information because of the sheer amount of information required to be put together.

To embed the graph there is several different techniques and each of them has different advantages and disadvantages.

*Matrix Factorization* is a possible way to do this and is good because it considers the global proximity which will give the analyst a more precise estimation of one vectors distance to all other vectors. The method does have a disadvantages in that it scales linear and can therefore be quite time consuming.

*Deep Learning* is very effective and robust which means that it can give good answers and can be very hard to infect with malware. There is also some disadvantages for example in how the system trains. It is possible to train the system so it will not need any feature engineering but can also be hit by overfitting and underfitting which can cause large problems for the system.

*Edge Reconstruction Based Optimization* is the term for three different methods "maximizing edge reconstruction, minimizing distance-based loss and minimizing margin-based loss" which in each there own ways ensure that the original graph input can be reconstructed from an embedded graph.

*Graph Kernel* starts in a kernel and then walks through a subgraph comparing each kernel that was chosen. This is mostly used in graph embedding and only represent and compare structures that are desired to be compared. But this method have problems with substructures that are not independent and will grow the size exponentially.

All these embedding strategies all have applications and can be used for a lot of different classification, clustering and recommendation methods. *Node Embedding* can be used for node classifications for SVM and KNN, node clustering in graphs and node recommendations by finding associations in the graph. *Edge Embedding* is used for triple classifications for example we can find if a relation a-b goes through relation r and finding which kind of link appears between two nodes in a graph. *Hybrid and Whole Graph Embedding* will make it possible to classify graphs in a lower dimension than they original were and this embedding method is better for visualization of the graph for human consumption.