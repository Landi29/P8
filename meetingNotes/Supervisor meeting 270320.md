## Supervisor meeting 27/03/20

### Agenda

* TET structure
  * Is the TET structure good enough?
    * A relation is in the papers only binary but our rating is a 3 valued relation. This would not be a big problem but it would change the definitions from the papers.
    * It all looks reasonable. 
    * Our figure needs to match our equations
    * We can either represent our genre with 3 distinct binary values which we would need a TET with 1 node for each different genre.
  * We should build our TET representations in networkx because it would be a better representations.
    * Could we reduce the amount of IO operations to reduce the time it takes to make a TET?
    * It shouldn't take longer than 2-3 hours. 
    * We could try and load all the data into a datastucture like a dictionary to speed things up
* What similarity metrics have you tried other than earth mover’s distance?
  * No other metric was used than Earth Mover Distance on histograms. There aren't really many other alternatives.
  * We don't need to look at other options for that particular use case.
  * There are multiple ways of using earth mover distance to get and overall similarity of TETs. 
* Embedding on a subgraph is done
  * What does it mean for the whole dataset?
    * It's infiesible to do node2vec on the entire dataset at once so splitting it up will make it better.
    * We need more RAM. Yell at ITS for more of it. 
    * The bottleneck is in the calculation of the probability.
    * We could generate random walks for all he subgraphs and feed them all into the learner that constructs the embedding.

### Questions

* SimRANK implementation
  * It take a bit of time to compute but it isn't too bad.
  * We may benifit from implementing SimRANK ourselves if we implement some kind of optimization. But only if the library aren't doing that themselves.
  * We should try and avoid going though all the data several times over. 

Next meeting at next friday same time as always. 



