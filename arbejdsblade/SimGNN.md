## SimGNN: A Neural Network Approach to Fast Graph Similarity Computation

In the article Bai. et al. presents a new method for computing graph similarity called SimGNN. They compare the method with other baseline similarity algorithms and conclude that their own method perform graph similarity quicker and more precisely than the other methods.

Similarity Computation via Graph Neural Networks (SimGNN) works by performing the following steps:

1. Convert pair of graphs into vectors.
2. Compute node-level embedding via GCN algorithm.
3. Compute graph-level embedding on a pair of graphs.
4. Compute Neural Tensor Network and pairwise comparison on the two graphs.
5. Insert the result from the two methods in the previous step into a feed forward neural networks which outputs a similarity score.

As mentioned above the first thing that happens is that graphs gets converted to vectors via node embedding. This is done via the Grap Convolution Networks (GCN) algorithm which is listed below:
$$
conv(u_n)=f_1(\sum_{m \in N(n)} \frac{1}{\sqrt{d_nd_m}}u_mW_1^{(l)}+b_1^{(l)})
$$
What happens here is is that we run the algorithm $conv(u_n)$ on a representation of a node $u_n$. Here $N(n)$ is the set of first-order neighbors of a node n plus n itself, $d_n$ is the degree of node n plus 1, $w_1^{(l)} \in \real^{D^1 \times D^{1+1}}$ is a weight matrix associated l-th GCN layer, $b_1^{(l)} \in \real^{D^{1+1}}$ is the bias and $f_1()$ is and activation function such as ReLU. Intuitively, the graph convolution operation aggregates the features from the first-order neighbors of the node. 

Once node embedding have been performed we have to compute the graph embedding. Here the important question is to figure out which nodes are more important than other. This is done via an attention mechanism that assigns weight to each nodes based on a similarity metric. The attention mechanism works as follows: 


$$
h= \sum^N_{n=1} \sigma(u^T_nc)u_n=\sum^N_{n=1}\sigma(u^T_ntanh((\frac{1}{N}\sum_{m=1}^Nu_n)W_2))u_n
$$
The idea behind this mechanism is that $u_n$ is the embedding of node n, $c$ is the global graph context which is computed by taking the average of all node embeddings  and feeding it into a nonlinear tranformation function: $c=tanh((\frac{1}{N}\sum_{m=1}^Nu_m)W_2)$ where $W_2$ is a learnable weight matrix. What $c$ provides is the structural and feature information that is adaptive to the given similarity via learning the weight matrix. Once $c$ has been computed we can begin computing once attention weight for each node. For node $n$, to make its attention $a_n$ aware of the global context, we take the inner product between $c$ and its node embedding. The intuition is that, nodes similar to the global context should receive  higher attention weights. We here apply a sigmoid function to ensure that the range of the attention weight is between 0 and 1. Lastly $h$ is the weighted sum of node embeddings $h= \sum^N_{n=1} a_nu_n$.

Once the graph-level embedding has been computed we can begin computing the relation between the two graphs. This is done via Neural Tensor Networks (NTN) which can be seen below:
$$
g(h_i,h_j) = f_3(h_i^TW_3^{[1:K]}h_j+V\begin{bmatrix}h_i \\ h_j \end{bmatrix} + b_3)
$$
Here $W_3^{[1:K]}$ is a weight tensorwhere [] denotes the concatenation operation, $V$ is a weight vector, $b_3$ is a bias vector and $f_3$ is an activation fucntion. K is a hyper parameter controlling the number of similarity scores produced by the model for each graph embedding pair. A limitation that this method has is that information such as graph size and feature distribution which is gained by performing node embedding can end up being lost when performing graph  embedding. In many cases the differences between two graphs lies in smalls substructures which are hard to reflect by graph-level embedding. Therefore we must also compute a finer level of relation between the two graphs which is done below.

Once NTN has been computed we begin computing the second method which is a pairwise node comparison.  This is computed as such $S = \sigma(U_iU_j^T)$ where $U_i$ and $U_j$ are node embedddings for the two graphs we are comparing and $\sigma$ is the sigmoid activation function. $S$ being the pairwise node similarity matrix. To gain some sort of ordering between graph nodes, the utilization of histograms are used.

Lastly the result of both pairwise node comparison and NTN are fed into a feed forward neural network which then outputs a similarity score. In the article they use the mean squarred error function as a loss function and train the NN supervised.

 The process of comparing two graphs can be seen in the figure below. 

![process](pictures\SimGNN\process.PNG)

