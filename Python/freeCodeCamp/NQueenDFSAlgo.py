def dfs_n_queens(n: int) -> list:
    #return a list of solutions;
    #each solution is itself a list of length n,
    #where the element at index i is the column index (0-based)
    #of the queen in row i.
    
    paths = []
    if n < 1 or n in (2, 3):
        return paths

    if n == 1:
        paths = [[0]]
        return paths

    """
    conditions:
    * a solution is a path which is a Eulerian cycle
    or Unconnected graph if has a loop ⟳ "node reconnect to itself":
            * each edge need just a weight = 1 : each edge must be counted only once
            in path( valid path ->solution).
            * no two share a
                -row: each node or element has exactly 1 ONE parent (one int edge)
                -column: each node or element has exactly 1 ONE child (one out edge)
                -diagonal: two consecutive nodes in adjacency matrix cannot be connected
                to a others consecutive nodes.
                           |__> for example : nodes 0 and 1 : (0--2) and (1--3)
                                                            or (0--3) and (1--2):
                             nodes consecutive 0 and 1 cannot have a relation with
                             a consecutive nodes like 2 and 3
    """
    def validated_path(adj_matrix, node):
        def is_line(adjacnecy_matrix, node):
            pass
        def is_column(adjacency_matrix, node):
            pass
        def is_diagonal(adjacency_matrix, node):
            pass
        return True
        #return not is_line(adj_matrix, node) and not is_column(adj_matrix, node) and not is_diagonal(adj_matrix, node)

    nodes = range(n)
    path = [0] * n
    adjacency_matrix = [[0] * n for _ in range(n)]
    # J'ai utilisé le for loop pour tester, but DFS work with stack then on utilise le while loop and stack =[]
    for x0 in nodes:
        path[0] = x0 # path = [x0= 0, x1, x2, x3, x4] for n= 5
        adjacency_matrix[0][x0] = 1
        # pour x0=node (node = 0, 1, 2 ,... ) on cherche tout valeurs possibles pour x1, puis x2, ...
        for x1 in nodes: # nodes = [node= (0, 1, 2, 3, 4)]
            if validated_path(adjacency_matrix,x1): #si la valeur de node x1 ne poduit pas mm ligne,colone,diagonale dans la matrix adjacence alors on fixe x1 comme fils valid pour sa racine x0 et on approfondir vers calculer ses fils de x1 (selon la methode DFS).
                path[1] = x1 # path = [x0= 0, x1, x2, x3, x4] for n= 5
                adjacency_matrix[1][x1] = 1
                # pour x1=node (validated_path(adjacency_matrix,node),node = 0, 1, 2 ,... ) on cherche tout valeurs possibles pour x2, puis x3, ...
                for x2 in nodes:
                    if validated_path(adjacency_matrix,x2): #si la valeur de node x2 ne poduit pas mm ligne,colone,diagonale dans la matrix adjacence alors on fixe x2 comme fils valid pour sa racine x1 et on approfondir vers calculer ses fils de x2 (selon la methode DFS).
                        path[2] = x2 # path = [x0= 0, x1, x2, x3, x4] for n= 5
                        adjacency_matrix[2][x2] = 1
                        # pour x2=node (validated_path(adjacency_matrix,node),node = 0, 1, 2 ,... ) on cherche tout valeurs possibles pour x3, puis x4, ...
                        for x3 in nodes:
                            if validated_path(adjacency_matrix,x3): #si la valeur de node x3 ne poduit pas mm ligne,colone,diagonale dans la matrix adjacence alors on fixe x3 comme fils valid pour sa racine x2 et on approfondir vers calculer ses fils de x3 (selon la methode DFS).
                                path[3] = x3 # path = [x0= 0, x1, x2, x3, x4] for n= 5
                                adjacency_matrix[3][x3] = 1
                                # pour x3=node (validated_path(adjacency_matrix,node),node = 0, 1, 2 ,... ) on cherche tout valeurs possibles pour x4
                                for x4 in nodes:
                                    if validated_path(adjacency_matrix,x4): #si la valeur de node x4 ne poduit pas mm ligne,colone,diagonale dans la matrix adjacence alors on fixe x4 comme fils valid -> x4 dernier fils -> x4 une feuille alors on reviens en arrière + on ajoutes path au paths (avec s) comme chemin valid.
                                        path[4] = x4 # path = [x0= 0, x1, x2, x3, x4] for n= 5
                                        paths.append(path)
                                adjacency_matrix[3][x3] = 0
                        adjacency_matrix[2][x2] = 0
                adjacency_matrix[1][x1] = 0
        adjacency_matrix[0][x0] = 0
    
    return len(paths)

print(dfs_n_queens(4))