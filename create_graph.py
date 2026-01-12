import matplotlib.pyplot as plt
import networkx as nx
from graph import Graph
from numpy import inf

constraints = ["1111"]

class GraphVisualization:
    def __init__(self):
        self.visual = []
        
    def add_edge(self, a, b):
        temp = [a, b]
        self.visual.append(temp)
        
    def visualize(self):
        G = nx.DiGraph()
        G.add_edges_from(self.visual)
        nx.draw_networkx(G)
        plt.show()
        
g = Graph()

k = max([len(c) for c in constraints])

suffixes = [""]

for i in range(k-1):
  new_suffixes = []
  for s in suffixes:
    if s+"0" not in constraints:
      new_suffixes.append(s+"0") 
    if s+"1" not in constraints:
      new_suffixes.append(s+"1") 
  suffixes = new_suffixes
   
for s in suffixes:
  g.add_node(s)
  for t in suffixes:
    if s + t[-1] not in constraints and s[1::] + t[-1] == t:
      g.add_edge(s, t)
    
adj = g.adjacency_matrix() 
adj_arr = []
for i, s in enumerate(adj):
  adj_arr.append([])
  rec = []
  for k in adj[s].keys():
    if adj[k][s] == 1:
      adj_arr[i].append(1)
      rec.append(f"{k}(n-1)")
    else:
      adj_arr[i].append(0)
  print(f"{s}(n)={'+'.join(rec)}")
      
g_vis = GraphVisualization()  
for e in g.edges():
  g_vis.add_edge(e[0], e[1])
g_vis.visualize()