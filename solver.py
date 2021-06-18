import networkx as nx
from parse import read_input_file, write_output_file
from utils import is_valid_network, average_pairwise_distance_fast
import sys


def solve(G):
    """
    Args:
        G: networkx.Graph

    Returns:
        T: networkx.Graph
    """

    def get_edges(arr):
        if len(arr) < 1:
            return None
        edges = []
        for i in range(len(arr) - 1):
            edges.append([arr[i], arr[i + 1]])
        return edges
    
    def eq_edges(edge1, edge2):
        return (edge1[0] == edge2[0] and edge1[1] == edge2[1]) or (edge1[0] == edge2[1] and edge1[1] == edge2[0])
    
    def add_freq(arr, edge):
        for e in arr:
            if (eq_edges(e[0], edge)):
                e[1] += 1
            
    edge_freq = [[(u, v, d['weight']), 0] for (u, v, d) in G.edges(data=True)]
    
    paths = []
    
    for node in nx.nodes(G):
        paths.append(nx.single_source_dijkstra_path(G, node, weight='weight'))
        
    for path in paths:
        for node in nx.nodes(G):
            for edge in get_edges(path[node]):
                if (edge != None):
                    add_freq(edge_freq, edge)
        
    edge_freq.sort(key = (lambda d: d[1]), reverse=False)
    
    t = nx.Graph()
    
    num_edges = nx.number_of_nodes(G) - 1
    added_edges = 0
   
    while (added_edges < num_edges):
        edge = edge_freq.pop()[0]
        #print(edge)
        #print(added_edges)
        t.add_edge(edge[0], edge[1], weight=edge[2])
        if (len(nx.cycle_basis(t)) > 0):
            t.remove_edge(edge[0], edge[1])
        else:
            added_edges = added_edges + 1
    
    return t


# Here's an example of how to run your solver.

# Usage: python3 solver.py test.in

if __name__ == '__main__':
    assert len(sys.argv) == 2
    path = sys.argv[1]
    G = read_input_file(path)
    #T = solve(G)
    #assert is_valid_network(G, T)
    print("Average  pairwise distance: {}".format(average_pairwise_distance_fast(G)))
    #if (nx.number_of_nodes(G) == 0):
    #    print(path)
    #    print("It's this one ^")
    #else:
    #print(path)

    name = path.split("/")
    name = name[1].split(".")
    write_output_file(G, "out/" + name[0] + ".out")
