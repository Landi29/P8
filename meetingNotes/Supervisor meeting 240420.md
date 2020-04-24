## Supervisor meeting 24/04/20

### Feedback on the paper

* What does logical paradigm mean? A bit confusing statement
  * We shouldn't see it as a programming language which we can catagorize. 
  * All the implementation has nothing to do with logical programming
  * The message might now bring any value to the paper and might bring more confusion.
  * We can either expand on the message or remove it.
* Are we doing 10 fold cross validation wrong?
  * We have to many bins
  * We don't really capture similarity well if we were to use euclidian or manhatten distance 
  * We need to take into account the similarity of the bins
  * Broadly speaking we a looking at the similarity of the roots in figure 1 but not the similarity of the children in figure 1
  * The similarity of the roots is based on the similarity of the children. We should take that into account
  * This can be considered an additional topic for future work. Maybe some prunning and such

### Question

* Graph embedding
  * Splitting method
    * The methods we have tried doesn't seem to work
      * We would need to implement our own graph splitting method but that costs time 
    * We could still try brute force method
      * We select 1 node randomly
      * In a few iterations we add neightbours untill we have reached a graph of a certain size
      * Then we take another random node and repeat the method again.
      * It wouldn't communicate any meaningful partition of the communities but at least we have tries to partion the graphs
      * It would be better than to give up
      * Could be used to construct some embedding and we can write in the appendix wheather it worked or didn't
* SimGNN
  * It works but takes a long time
    * We wouldn't be able to make the 10 fold cross validation
      * We can also try 1 or 2 fold since that is what we could compute 
    * We could ask for more resources
    * We can try some method such as adding GPU or multiprocessing
* We can try and run all of our method on a small subset of the data. Would be a good stategy for finding more errors.

Meeting is next week same time.

