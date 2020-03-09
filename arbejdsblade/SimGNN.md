## SimGNN: A Neural Network Approach to Fast Graph Similarity Computation

In the article Bai. et al. presents a new method for computing graph similarity called SimGNN. They compare the method with other baseline similarity algorithms and conclude that their own method perform graph similarity quicker and more precisely than the other methods.

Similarity Computation via Graph Neural Networks (SimGNN) works by performing the following steps:

1. Convert pair of graphs into vectors via GCN.
2. Compute graph-level embedding on a pair of graphs.
3. Compute Neural Tensor Network and pairwise comparison on the two graphs.
4. Insert the result from the two methods in the previous step into a feed forward neural networks which outputs a similarity score.



