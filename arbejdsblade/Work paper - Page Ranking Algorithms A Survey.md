# Page Ranking Algorithms: A Survey
PageRank is an algorithm used by Google that ranks web pages. The algorithm counts the number and strength of links to a page to estimate the importance of a it. 

The simplest way of calculating is $PR(A)={\frac {PR(B)}{L(B)}}+{\frac {PR(C)}{L(C)}}+{\frac {PR(D)}{L(D)}}$ where PR(x) is the PageRank of a given page an L(x) is the number of outbound links from a page. More specifically $PR(u)=\sum_{v \in B(u)}^{10} \frac {PR (v)}{L(v)}$ where B(u) is the set of pages pointing to u.

In later research it was observed that just because there is a link, it does not mean that a user uses it. The algorithm was modified with a dampning factor d. 

$PR(u) = (1 - d) + d* \sum_{v \in B(u)} \frac {PR (v)}{L(v)}$

This approach of the PageRank is meant to be done over several iterations, all PageRank can be assigned statically or randomly and will normalize over the iterations. Having a high PageRank is a good.

This is mostly used for web structure mining or mining other graph structures for importance. Implemented correctly, this algorithm can have a complexity of $O(log(N))$.

The algorithm has been further enhanced by incorporating weights of ingoing and outgoing links, and was rebranded as weighted PageRank.
The weight link(u,v) with incoming links of page u and the incoming links of all reference pages of page v

$W_{(v,u)}^{in} = \frac{I_u}{\sum_{p \in R(v)}I_p}$

I is the number of incoming links of page u and v, R(v) is the list of reference links of page v.

$W_{(v,u)}^{out} = \frac{O_u}{\sum_{p \in R(v)}O_p}$

O represents the number of outgoing links of u and p

$WPR(u) = (1 - d) + d* \sum_{v \in B(u)}WPR(v)*W_{(v,u)}^{in}*W_{(v,u)}^{out}$

The algorithm is then altered to incorporate to the form above.

This algorithm has the same properties as the original, but its results are of a higher quality.
