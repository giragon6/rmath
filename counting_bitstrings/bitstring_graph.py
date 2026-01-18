import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import sympy as sp
from matplotlib.figure import Figure

class BitstringGraph:
  def __init__(self, constraints):
    self.constraints = constraints
    self.g = nx.DiGraph()
    
    lengths = [len(c) for c in constraints]
    k = max(lengths)
    unique_lengths = list(set(lengths))

    self.suffixes = [""]

    # horrifically inefficient method 
    # we need to include suffixes even if they're invalid
    # for the characteristic polynomial method of recursive
    # generation to work
    for i in range(k-1):
      new_suffixes = []
      for s in self.suffixes:
        new_suffixes.append(s+"0")  
        new_suffixes.append(s+"1") 
      self.suffixes = new_suffixes
      
    for s in self.suffixes:
      self.g.add_node(s)
      for t in self.suffixes:
        valid = True
        for l in unique_lengths:
          if (s in constraints
              or s[l-1::]+t[-1] in constraints 
              or (len(s) == l-1 and s+t[-1] in constraints)
              or not s[1::] + t[-1] == t):
            valid = False
        if valid:
          self.g.add_edge(s, t)
          
    self.adj = nx.to_dict_of_lists(self.g)
    
    self.npadj = nx.to_numpy_array(self.g)
    
    self.recs = {(s,0): [] for s in self.adj}
      
    for s in self.adj:
      for k in self.adj[s]:
          self.recs[(k,0)].append((s,1))
    
  def show(self):
    nx.draw_networkx(self.g)
    plt.show()
    
  def to_cytoscape(self):
    nodes = [{"data": {"id": n}} for n in self.g.nodes()]
    edges = [{"data": {"source": u, "target": v}} for u, v in self.g.edges()]
    return {"nodes": nodes, "edges": edges}
    
  def print_recs(self):
    # this prints the recursive equations for each suffix
    for s in self.recs.keys():
      print(f"{s[0]}(n)={'+'.join([f"{r[0]}(n-{r[1]})" for r in self.recs[s]])}")        
  
  def get_recursive(self):
    # the degrees of the characteristic polynomial give us the recursive equation
    # e.g., for 000, the characteristic polynomial is λ^4-λ^3-λ^2-λ^1=0
    # invoking umbral calculus gives us λ_4-λ_3-λ_2-λ_1=0
    # define n=4 to get λ_n=-λ_n-1+λ_n-2+λ_n-3, our recursive
    # to get the characteristic polynomial of the adjacency matrix A,
    # we need to compute the determinant of A-λI
    # (i.e., A minus a "diagonal" of lambdas)
    # since we need to use a symbol, lambda, we'll use sympy
    npid = np.identity(self.npadj.shape[0])
    spid = sp.Matrix(npid) # I
    spadj = sp.Matrix(self.npadj) # A
    lam = sp.Symbol("l") # λ
    
    lambda_id = lam * spid # λI
    M = spadj - lambda_id # A-λI
    det = sp.poly(M.det()) # convert to polynomial to find degree
    
    degree = sp.degree(det) # highest degree
    # now we need to make all the superscripts into subscripts
    # and put all degrees in terms of n
    # so that sympy understands, let's replace lambda with a function x(n)
    # such that x_n or x(n) is the number of valid bitstrings of length n
    x = sp.Function('x')
    n = sp.Symbol('n')
    rec = det
    for i in reversed(range(1,degree+1)):
      rec = rec.subs({lam**i:x(n-sp.Integer(degree-i))})
   
    solved_for_xn = sp.solve(rec, x(n), dict=True)
    # yippee! now we have a recursive!
    return solved_for_xn
    
  def get_sequence(self):
    pass
  
if __name__ == "__main__":
  bs = BitstringGraph(["000","11"])
  bs.get_recursive()
  bs.show()