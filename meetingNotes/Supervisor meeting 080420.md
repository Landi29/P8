## Supervisor meeting 08/04/20

### Node2vec

* Run random walks on all the subgraphs and then embed it on those. 
* The transistion matrix shouldn't be larger than the graph. 
* It should release the memory from one iteration to another which our code does not which is where the problem might be.
* It sounds like that their code doesn't release the code. It sounds like the library we are using a bit screwed.
* Node2vec has 2 parameter, alpha and beta, there should be a setting where they become a uniform. We should try that setting. It should make our transition probabilities uniform and save on space.
* We could devide our random walk up on smaller graphs and feed the list of walks to the embedder.
  * The collection of random walks should be as similar to the random walks we would have gotten in the full graphs.
  * The alpha and beta parameters determine how the random walks look like.  There are settings that make the random walks more local and setting that make them more exploratory. 
  * The strategy for deviding the graph depends on the stucture which we should study and figure out
  * We could try some standard graphs clustering/segmentation algorithms which tries to connect the graph into a bunch of tightly connected subgraphs. 
    * The subgraphs would overlap (i.e. have some nodes in common)
    * Networkx might provide some graph segmentation options.
  * We could cut the graph up which networkx support
    * Spectral clustering is a form of cutting
    * We need to remember the edges between the nodes where the cut took place
    * We can use a standard segmentation/cutting algorithm to cut the graph into 15-20 pieces.
      * For each component we have created we add the 1 or 2 hop neighbors.
    * It's all experimentation so no right or wrong answers.
    * This could in itself be our entire research if we want.

### TET

* Comparing TETs with KNN is pretty slow
  * We are trying to cluster the TETs and compare on the clusters to speedup performance
* If we had to compare every TETs with every TET it would take a year to do. Recommending would only take a few minuttes.
* They used the metric tree data structure which we could look into and cut down the computation time by a lot.
* Manfred needs more information on what we are doing.

### SimGNN

* SimGNN doesn't support edge labeling. Would it be worth to try and make it support it.
* If we can get some data that is close then we don't need to change anything. 
* We can keep it in our backlog and try to make it work if we wanted to. 
  * We could puplish that as a paper itself
* If we can make it work on our graphs and get some useful data it could still be valuable information.
* We shouldn't focus on extending SimGNN code.
* We could also try to code the edge label as nodes. 
* User -rating label> product
  * User -> rating node -> product
* Extending SimGNN could be interesting purposal.
  * They could potentially support that
  * Manfred and Dolog will be supervising together
  * Deadline is on Tuesday next week

### AOB

Consultation will be on the 20th of April

Next meeting will be on Friday next week