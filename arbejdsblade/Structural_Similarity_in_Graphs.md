# Structural Similarity in Graphs
## Notes for the paper Structural Similarity in Graphs* A Relaxation Approach for Role Assignment
Given a graph one tries to assign roles to vertices by looking for partitions of the vertex set such that equivalent vertices can be considered to occupy the same kind of structural position.
Vertices can have the same role if they are structurally equivalent, i.e. they have identical neighborhoods.
However, practical applicability of these kinds of vertex partitions to social networks or other irregular graphs is severely limited. (See paper for details).
In social networks and other graphs in which many pairs of vertices are
somehow related, but not exactly equivalent, we need a notion of similarity of
vertices, rather than equivalence.

### Graph spaces:
We associate a graph $G = (V,E)$ with the vertex space $\mathcal{V} := \mathcal{V}(G) :=
{f : V \rightarrow \mathbb{R} }$, that is the vectorspace of all real-valued functions on the vertex set.


### Structural Similarities:
For an equivalence relation $\sim$ on the vertex set $V$ of a graph $G = (V,E)$, let $W := V / \sim$ be its set of equivalence classes.

The associated surjective mapping $φ : V \rightarrow W$, that maps vertices to their equivalence class, defines a binary $|W| \times |V|$ matrix $P$ where for $v \in V$ , $w \in W$, $P_{wv} = 1$ iff $φ(v) = w$.
Relaxations of such class mappings allow for the entries $p_{wv}$, instead of $1$’s
(“$v$ is in class $w$”) and $0$’s (“$v$ is not in class $w$”), real numbers (“$v$’s degree of
membership to $w$ is $p_{wv} \in \mathbb{R}$”).

**Definition 3:** Let $\mathcal{V}$ and $\mathcal{W}$ be two euclidian vectorspaces. A surjective linear homomorphism $\pi: \mathcal{V} \rightarrow \mathcal{W}$ is called a projection if $\pi \pi^T = id_\mathcal{W}$.

*Note to Definition 3: A homomorphism in algebra is a structure-preserving map between two algebraic structures of the same type. Homomorphisms of vector spaces are also called linear maps. A linear map is then a mapping between two vector spaces $V \rightarrow W$ that preserves the operations of addition and scalar multiplication. The linear map $\pi$ is then surjective, if for all $w \in W$, there is at least one element $v \in V$ such that $\pi(v) = w$*

**Matrix transpose:** In linear algebra, the transpose of a matrix $A$ is an operator which flips a matrix over its diagonal such that the row and column indices of the matrix are switched. This produces a new matrix, called the transpose of $A$, denoted as $A^T$. Here, the rows of $A$ become the columns of $A^T$ and the columns of $A$ become the rows of $A^T$. 

**Matrix transpose example:** 
$$

A =
    \begin{bmatrix}
        1 & 2\\
        3 & 4\\
        5 & 6\\
        7 & 8
    \end{bmatrix}, \,

    A^T = 

    \begin{bmatrix}
        1 & 3 & 5 & 7\\
        2 & 4 & 6 & 8
    \end{bmatrix}
$$

We define similarities as relaxations of equivalence relations, such that similarities and projections are associated with each other just like equivalence and class membership relations.

Let $φ : V \rightarrow W$ be a surjective mapping and $P$ be the (binary) characteristic matrix of $φ$.

The equivalence relation induced by $φ$ has characteristic matrix $S = P^T P$ , since two vertices $u$ and $v$ are equivalent, iff the corresponding columns of $P$ have the $1$ in the same row, i.e. $s_{uv} = 1$.

If we relax $P$ to a projection $\pi$, then $\sigma := π^T π$ is symmetric, i.e. $\sigma^T = \sigma$, and
idempotent, i.e. $\sigma^2 = \sigma$ and these properties serve to define our relaxation of equivalence relations.

**Definition 5:** For a euclidian vectorspace $\mathcal{V}$ an endomorphism $\sigma : \mathcal{V} \rightarrow \mathcal{V}$ is called a similarity if it is symmetric, i.e. $\sigma^T = \sigma$, and idempotent, i.e. $\sigma^2 = \sigma$.

An equivalence relation $\sim$ induces a similarity represented by the matrix $S_\sim$ ,called here the *normalized matrix* of $\sim$, which is given by:

$$
    (S_\sim)_{uv} := 
    \begin{cases}
        0 \quad \text{if} \ u \not \sim v \\
        1/c \quad \text{if} \ u \sim v \quad \text{and} \ c \  \text{is the size of the equivalence class of} \ v
    \end{cases}
$$
