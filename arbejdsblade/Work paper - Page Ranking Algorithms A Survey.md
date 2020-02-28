# Page Ranking Algorithms: A Survey
PageRank is an algorithm used by Google that ranks web pages. The algorithm counts the number and strength of links to a page in order to estimate the importance of it. 

The simplest way of calculating the PageRank of a page is given by the formular:

 $PR(A)={\frac {PR(B)}{L(B)}}+{\frac {PR(C)}{L(C)}}+{\frac {PR(D)}{L(D)}}$ 
 
 Where PR(x) is the PageRank of a given page and L(x) is the number of outbound links from a page (A, B, C and D are pages in the formular above). A more general difinition is given by this formular:
 
$PR(u)=\sum_{v \in B(u)}^{10} \frac {PR (v)}{L(v)}$ 

where B(u) is the set of pages pointing to page u.

In later research it was observed that just because there is a link, it does not mean that a user uses it. The algorithm was modified with a dampning factor d. 

$PR(u) = (1 - d) + d* \sum_{v \in B(u)} \frac {PR (v)}{L(v)}$

This approach to PageRank is meant to be done over several iterations, where all PageRanks can be assigned statically or randomly and will normalize over the iterations. Having a high PageRank is good.

This is mostly used for web structure mining or mining other graph structures for importance. Implemented correctly, this algorithm can have a complexity of $O(log(N))$.

The algorithm has been further enhanced by incorporating weights of ingoing and outgoing links, and was rebranded as weighted PageRank.
The weight link(u,v) with incoming links of page u and the incoming links of all reference pages of page v

$W_{(v,u)}^{in} = \frac{I_u}{\sum_{p \in R(v)}I_p}$

I is the number of incoming links of page u and v, R(v) is the list of reference pages from v. In lay man’s terms it is a list of every reference to or from v, but in the terms of the calculation for ingoing weight then R(v) is ingoing links and for outgoing weight it the outgoing links.

$W_{(v,u)}^{out} = \frac{O_u}{\sum_{p \in R(v)}O_p}$

O represents the number of outgoing links of u and p. 

The two formulas above are formulas for calculating the weight of incoming links $W_{(v,u)}^{in}$, and weight of outgoing links $W_{(v,u)}^{out}$ for every refence page v to for from page u.

$WPR(u) = (1 - d) + d* \sum_{v \in B(u)}WPR(v)*W_{(v,u)}^{in}*W_{(v,u)}^{out}$

The algorithm is then altered to incorporate to the form above and as mentioned is the formula for Weighted PageRank(WPR).

This algorithm has the same properties as the original, but its results are of a higher quality.
