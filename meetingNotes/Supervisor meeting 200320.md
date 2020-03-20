## Supervisor meeting 20/03/20

#### Agenda

* State of the project
  * We don't need to use networkx for clutering we can just create a vector that represent the tags with dimensionality for all movies and then use k-means, scikit or some other library for clustering (we do need to experiment with figuring out how many clusters we want).
  * The vectors will be large and have many dimensions.
  * We could also look up word embeddings where we can type in our tag and get a vector representation of it which we can cluster on
    * word2vec
      * Would need to be trained
      * http://bionlp-www.utu.fi/wv_demo/
  * We don't want to do the embedding ourselves we want to find some tools that can do it for us.
  * An alternative we could create a co-occurence metric for each tag and do spectral clustering.
    * Will be a squared dimension of tags
    * Laplasian will give us an eigen vectors
    * Will give an embedding of the tags at a lower dimensionality
    * Would be viable for our case
    * We want to find the community of tags that belong to each other
    * https://link-springer-com.zorac.aub.aau.dk/article/10.1007/s11222-007-9033-z
      * Find eigen vectors and then cluster and then run k-mean over it
  * If we could run k-means on the high dimensionality vectors that would be effecient enough. 
* Node2vec implementation
  * NetworkX is not a good data structure to work on because it's very object oriented
  * Takes 10 min to run on each node and we have over 10k nodes
    * The run time per node is most likely for computing random-walk
  * We should not try to run node2vec that hasn't been tested
  * Could be a hardware difference
    * We should try and run it on the virtual server to see if it will perform better.
  * We could also experiment with different libraries but it's hard to say what is best to do.

#### Paper feedback

* Feedback to the paper will not be very suffecient because the paper will still change a lot.
* It's good that we have a preliminary.
* We used the survey paper a lot and rephrase
* We have very textual definitions
  * But it depends on what we need
  * If the report will be a lot of written text then we won't need definitions
* It's difficult to advise anything right now since the report is still very early in the states
* Do continue writing.
* Write more work papers

#### Other things

* Will the quarantine be extended?
  * Jokes on us, they don't know
  * Don't expect things to change for the next few weeks
  * Everything is still in the air but we need to be prepared for it
  * From how the current situation is:
    * THIS
    * IS 
    * JUST 
    * THE 
    * BEGINNING
    * !!!
    * https://www.youtube.com/watch?v=pdRH5wzCQQw
* Meeting next week, same time