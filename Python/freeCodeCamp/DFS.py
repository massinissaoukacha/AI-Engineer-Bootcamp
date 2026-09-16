"""
[ 0  1  2  3
0[0, 1, 0, 0],
1[1, 0, 1, 0],
2[0, 1, 0, 1],
3[0, 0, 1, 0]
], 1)
"""
adj_matrix = [
    [0, 1, 1, 0, 0, 0, 0],
    [1, 0, 0, 1, 1, 0, 0],
    [1, 0, 0, 0, 0, 1, 1],
    [0, 1, 0, 0, 0, 0, 0],
    [0, 1, 0, 0, 0, 0, 0],
    [0, 0, 1, 0, 0, 0, 0],
    [0, 0, 1, 0, 0, 0, 0]
    ]

def dfs(adj_matrix, node_label):

    #An undirected, adjacency matrix.
    #A node label, which is the numeric value of the node between 0 and n - 1,
    #where n is the total number of nodes in the graph.

    total_nodes = len(adj_matrix)
    if node_label < 0 or node_label >= total_nodes :
        return f'The node label value must be a numeric between 0 and {total_nodes - 1}'

    stack = [node_label]
    visited = [node_label]
    path = []
    print('pile: ',stack)
    print('visité: ',visited)
    print('path: ',path)
    while len(stack) > 0:
        node_poped = stack.pop()
        print('node à empiler:',node_poped)
        path.append(node_poped)

        #voisins de l'element empiler & not in visited
        voisins_non_visites = [node for node, value in enumerate(adj_matrix[node_poped]) if value != 0 and node not in visited]
        visited.extend(voisins_non_visites)
        voisins_non_visites.reverse()
        stack.extend(voisins_non_visites)
        
        print('pile: ',stack)
        print('visite: ',visited)
        print('path: ',path)

    return path

print(dfs([[0, 1, 0, 0], [1, 0, 0, 0], [0, 0, 0, 1], [0, 0, 1, 0]], 0))