# Structural Similarity in Graphs
## Notes for the paper Structural Similarity in Graphs* A Relaxation Approach for Role Assignment
Given a graph one tries to assign roles to vertices by looking for partitions of the vertex set such that equivalent vertices can be considered to occupy the same kind of structural position.
Vertices can have the same role if they are structurally equivalent, i.e. they have identical neighborhoods. 
However, practical applicability of these kinds of vertex partitions to social networks or other irregular graphs is severely limited. (See paper for details).
In social networks and other graphs in which many pairs of vertices are
somehow related, but not exactly equivalent, we need a notion of similarity of
vertices, rather than equivalence.

### Graph spaces:
We associate with a graph $G = (V,E)$ the vertex space $\mathcal{V} := \mathcal{V}(G) :=
{f : V \rightarrow \mathbb{R} }$, that is the vectorspace of all real-valued functions on the vertex
set. 


### Structural Similarities:
For an equivalence relation ~ on the vertex set $V$ of a graph $G = (V,E)$, let $W := V / ~ $ be its set of equivalence classes.

The associated surjective mapping $φ : V \rightarrow W$, that maps vertices to their equivalence class, defines a binary $|W| \times |V|$ matrix $P$ where for $v \in V$ , $w \in W$, $P_{wv} = 1$ iff $φ(v) = w$.
Relaxations of such class mappings allow for the entries $p_{wv}$, instead of $1$’s
(“$v$ is in class $w$”) and $0$’s (“$v$ is not in class $w$”), real numbers (“$v$’s degree of
membership to $w$ is $p_{wv} \in \mathbb{R}$”).