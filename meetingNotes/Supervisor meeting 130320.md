## Supervisor meeting 13/03/20

### Questions

* How to best find and represent the subgraphs in for the recommendations. We discussed using a tree representation inspired by type extension trees or a vector representation but are not sure how we would be able to contain the  relevant data most efficiently and not using to much memory space?
  * Depends on the method what we want to use.
  * What is the data? What information do we have? What are the attributes?
  * We probably want to predict if a user would like a specific movie?
    * In terms of embedding there are some that only uses the graph and not the information stored in the nodes such as random walk.
    * How do we store the node attributes when converting the graph to vectors?
    * GNN can take node attributes?
  * The choice of method all comes down to what we want to do.
* How do we want to exploit strucutural similarity in terms of recommendation systems?
  * We can also binarise the data
  * What kind of similarities do I want to base my recommendations on. The choice of this can help determine the method
* Look into tag genome in the movielens article.
  * Mapping a tag to a movie
  * We can collect additional data from IMDB via their api.
    * Could give us a richer stucture
  * Can be used to track it back to a user
  * Relevance between movie and tag
  * Would be too much for TET
    * Would be infeasible but it could be scaled down 
  * Would allow us to get information about users.
  * We could try clusering the tags to reduce it's size and identify these tag clusters.
    * These tag clusters could be uses as attributes

* Do you expect us to be using TET as a way to find similarities between substructures or will we strictly be looking at current methods using graph embedding and using similarity measures on those?
  * We need some baselines to compare against.
  * Can we implements a simple idea of TET and write about it
  * We won't be using all the area of TET only the basic idea.
  * We could compare pure Node2Vec agains our simple TET or TET inspired similarity structure.
* We could always place attributes as nodes. But it would not make a big difference compared to the other suggestions.
* Graph embedding as a concept edges should point both ways?
  * Depends on the context.
  * Node2Vec which simply embeds node to euclidean space can't be turned into a node to a graph.
  * We should not need to reverse anything?
  * Send Manfred some sources so he can confirm better.

### Other things

What can we promise them for next week?

* They will get the first draft of our paper
* Have we started to experiment?
* Start experimenting with methods now!

Next meeting on friday same time.

