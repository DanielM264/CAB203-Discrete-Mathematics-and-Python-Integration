# get a single element of a set. Don't care which
def arbitraryElement(S):
    return next(iter(S))

# vertices connected by an edge from u.
def N_out(V, E, u):
    return { v for v in V if (u,v) in E }

# vertices connected by an edge from S.
def NS_out(V, E, S):
    return { v for v in V for u in S if (u,v) in E }

# vertices connected by an edge to u
def N_in(V, E, u):
   return { v for v in V if (v,u) in E }

# vertices connected by an edge to S
def NS_in(V, E, S):
    return { v for v in V for u in S if (v,u) in E }

def distanceClasses(V, E, u):
   """Given a graph (V,E) and a starting vertex u, outputs a list of distances classes.  That is, returns a partition of the vertices into sets of fixed distances from u, where u is in the distance class for distance 0.  Behaviour is undefined if the graph is disconnected.
   
   This version differs from that in graphs.py in that when the graph is directed then all paths considered follow the direction of edges.  For example, D[1] is the set of vertices v where there is an edge from u to v.  Edges from v to u are not considered.
   """
   V0 = V              # V_0 = V
   D = [ {u} ]         # D[0] = D_0 = {u}
   return distanceClassesR(V0, E, D)

def distanceClassesR(V, E, D):
   Vnew = V - D[-1]            # V_{j} = V_{j-1} / D_{j-1}
   if len(Vnew) == 0: return D # Already considered all elements?
   Dnew = D + [ NS_out(Vnew, E, D[-1]) ]  # D_{j} = N_{V_j}(D_{j-1})
   return distanceClassesR(Vnew, E, Dnew)

def hasInEdge(V, E, v):
   """Given a directed graph (V, E) and a vertex v, return whether v has any edges going into it."""
   return len(N_in(V, E, v)) != 0

def topOrdering(V, E):
   """Given a directed graph (V, E) return a topological ordering if it exists, otherwise returns False."""
   return topOrderingR(E, set(), V, [])    # G0 = {}, V0 = V

def topOrderingR(E, G, V, ordering):
   Gnew = { v for v in V if not hasInEdge(V, E, v) }
   if len(Gnew) == 0: return False         # there must be a cycle
   ordering = ordering + [ u for u in Gnew ]
   Vnew = V - Gnew
   if len(Vnew) == 0: return ordering      # no more vertices
   return topOrderingR(E, Gnew, Vnew, ordering)

def findPath(V, E, start, end, path = None):
   """Given a (directed) graph (V,E), outputs a list of vertices forming a (directed) path from start to end.  If no such path exists, returns None.
   
   Implemented using a simple DFS algorithm."""
   # Take care of starting case so user doesn't have to supply the empty path
   if path is None: path = [ start ]  
   
   # Base case:
   if start == end: return path

   # Search through neighbours.  Ignore vertices that are already on the path 
   # so we don't create a cycle.
   for v in N_out(V, E, start):
      if v in path:
         continue
      path.append(v)
      # try to find end by going through v.  If we do, then we have found the path.
      r = findPath(V, E, v, end, path)
      if r is not None: return path
      path.pop()

   # If we haven't returned yet, then we can't find the end going this direction.
   return None

def augmentingEdges(V, E, w, f):
   """Given an anti-symmetric directed graph, edge weights w, and a valid flow f, returns an edge set representing edges that can be in an augmenting path. """
   # forward edges
   E1 = { (u,v) for (u,v) in E if f[(u,v)] < w[(u,v)] }

   # backward edges
   E2 = { (v,u) for (u,v) in E if f[(u,v)]  > 0 }
   return E1 | E2

def augmentingPath(V, E, w, f, s, d):
   """Given an anti-symmetric directed graph, edge weights w, and a valid flow f, source vertex s and drain vertex d, returns an augmenting path as a list of vertices."""
   Enew = augmentingEdges(V, E, w, f)
   return findPath(V, Enew, s, d)


def edgeCap(w, f, u, v):
   """Given edge weights w, flow f, and edge (u,v), returns the augmenticy capacity of the edge."""
   if (u,v) in f:
      return w[(u,v)] - f[(u,v)]

   return f[(v,u)]

def augmentingPathCapacity(path, f, w):
   """Given an augmenting path, edge weights w and a valid flow f, returns the capacity of the augmenting path."""
   cap = edgeCap(w, f, path[0], path[1])

   # search over all edges in the path
   for (u,v) in zip(path[1:-1], path[2:]):
      ecap = edgeCap(w, f, u, v)
      cap = ecap if ecap < cap else cap

   return cap

def augmentFlow(path, f, w):
   """Given an augmenting path, edge weights w and a valid flow f, returns a valid flow g augmented along the augmenting path."""
   g = dict(f)
   a = augmentingPathCapacity(path, f, w)
   for u,v in zip(path[:-1], path[1:]):
      if (u,v) in f:         
         g[(u,v)] = f[(u,v)] + a
      else:
         g[(v,u)] = f[(v,u)] - a
   return g

def maxFlow(V, E, w, s, d):
   """Given an anti-symmetric directed graph, edge weights w, a valid flow f, source vertex s and drain vertex d, returns a maximum flow. """
   f = { e: 0 for e in E }  # initial flow all 0

   # augment along augmenting paths as long as we can
   while (path := augmentingPath(V, E, w, f, s, d)) is not None:
      f = augmentFlow(path, f, w)
   return f

if __name__ == "__main__":
   V = { 1, 2, 3, 4, 5, 6 }
   w = { (1, 2): 3, 
         (2, 3): 2,
         (3, 6): 3,
         (1, 4): 2,
         (4, 5): 2,
         (5, 6): 2,
         (2, 4): 2,
         (3, 4): 2,
         (5, 3): 2 }
   E = set(w.keys())
   s = 1
   d = 6
   print(maxFlow(V, E, w, s, d))
