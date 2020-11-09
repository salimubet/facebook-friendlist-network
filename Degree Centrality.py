import networkx as nx
import colorlover as cl
import numpy as np
import pickle
import copy
import matplotlib.pyplot as plt

# This is your Facebook id. It can also be a number
CENTRAL_ID = 'FACEBOOK_ID'

# This is the pickle file containing the raw graph data
GRAPH_FILENAME = 'mutuals'

# Load the friend_graph picklefile
with open(GRAPH_FILENAME, 'rb') as f:
    friend_graph = pickle.load(f)

# Only keep friends with at least 2 common friends
central_friends = {}

for k, v in friend_graph.items():
    # This contains the list number of mutual friends.
    # Doing len(v) does not work because instead of returning mutual
    # friends, Facebook returns all the person's friends
    intersection_size = len(np.intersect1d(list(friend_graph.keys()), v))
    if intersection_size > 2:
        central_friends[k] = v

print('Firtered out {} items'.format(len(friend_graph.keys()) - len(central_friends.keys())))

# Extract edges from graph

edges = []
nodes = [CENTRAL_ID]

for k, v in central_friends.items():
    for item in v:
        if item in central_friends.keys() or item == CENTRAL_ID:
            edges.append((k, item))

G = nx.grid_2d_graph(3, 3)

G.add_nodes_from([CENTRAL_ID])
G.add_nodes_from(central_friends.keys())

G.add_edges_from(edges)
print('Added {} edges'.format(len(edges) ))

pos = nx.spring_layout(G) # get the position using the spring layout algorithm

# remove myself from the graph
G_f = copy.deepcopy(G)
G_f.remove_node(CENTRAL_ID)

# keep the position
pos_f = copy.deepcopy(pos)
pos_f.pop(CENTRAL_ID, None)

# Degree centrality
degree = nx.degree_centrality(G_f)
values_degree = [degree.get(node)*500 for node in G_f.nodes()]

# Degree centrality
plt.subplot(221)
nx.draw_networkx(G_f, pos =pos_f,
                 cmap = plt.get_cmap('Reds'),
                 node_color = values_degree, node_size=values_degree,
                 width=0.2, edge_color='grey', with_labels=False)
#limits=plt.axis('off') # turn of axisb

plt.savefig("graph.png", dpi=1000)
plt.show()
