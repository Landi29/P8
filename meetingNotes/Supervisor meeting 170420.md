## Supervisor meeting 17/04/20

### Question

* Have we tried all of the different cutting algorithm on our graphs?
  * Try the networkx cutting methods
  * We need to know how big our cuts can be
  * We need some sort of balanced cutting algorithm that can create equal sized subgraphs
  * Normalized cut algorithm should work. If not then we can try Mean cut
  * We can also try k-clique
    * We have to specify k but this could be a problem for our use case
  * We can also try clustering.
* Should we remove users with large amounts of ratings?
  * Active users could be valuable for us from a recommender perspective
  * You normally don't remove users with large amounts of data
  * Normally we could remove inactive users instead due to them not contributing much if anything.
  * We can argue that both extremes can be bad for us
  * Removing the top 2% and buttom 2% could be more representative.
  * Most recommender systems don't touch the top users
  * It's up to us and we need to argue for why we would do it.
  * Could give the different recommendations
  * Removing the long tail would be more benificial. Cutting away non acitve users.
  * Even if our users have 20 rating we could still raise the bar a bit
  * Cutting inactive users tends to lead to a removal of more users than remove the top.
  * We can argue that removing the top users decreses the popularity bias
  * We can write a bit of data analysis down such that it can be described at the exam.
* TET's 
  * It's going good
* SimGNN
  * Everything is going great. We just need to get the server up and running.
  * Some reflections working on SimGNN could be added into the appendix of the paper since it doesn't fit into the actual paper but it's an important learning experience.
* Appendix paper
  * Would be a good idea of writing down of our reflections of what we have learned in the appendix would be a good idea.
  * Doesn't need to be super refined.

### Experimentation phase

* There are subtleties that we need to take care of and explain.
  * Do we devide the data on the node level or the edge level?
  * This determines what would we be testing?
* Leave-one-out method
* Splitting the data into folds
* Recommender Systems handbook. Read the chapter on evaulating recommender systems.
* We should have that sorted by next week how we want to evaluate our recommender systems

### Other

Next week same time on MS Teams

