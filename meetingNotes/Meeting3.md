# Meeting notes for meeting 3.

## Movielens data set

* Some methods only work on plain graphs and cannot use additional attributes. 
* Extensions to node2vec that uses attributes. Not most common way. 
* Graph neural networks can take node attributes.

What methods to use is integrated with what we want to do.
Think about how we want to exploit the structural similarity for standard recommendation tasks. 


For a given user: Find similar users.

For structural similarity: Have the users rated movies with similar attributes (not the same movies).
Either keep the rating values or categorize them.

* What do we want to recommend.
* How do we want to recommend it: 
  * Here we must use the relevant theory tools.
* Movielens tags (mentioned by Peter) as aditional attributes.
  * Structure of these tags. 
  * 1100 attributes may be too much for TET.
  * But one can take some ideas from TET and use them or use less attributes. 
  * We can do clustering on the movie tags and identify 50 to 100 tag clusters and use them as attributes.
  * The score would be the average score of the tags in each cluster. 

## Our task
Use some of the ideas from TET (make a simpler version of TET) for recommendation and compare the result with other methods such as node2vec and graph embedding. 

## Discussion of encoding graphs
* Vectors in node2vec cannot be reversed to graph nodes again. 
* It is possible to learn a decoding function.
* Work in parallel on theory and implementation.
