def adjacency_list_to_matrix(adjacency_list: dict) -> list:
    #adjacency_list -> adjacency matrix
    #print each for each in adjacency matrix
    #return adjacency matrix
    """ example :
            adjacency list = {
                0: [2],
                1: [2, 3],
                2: [0, 1, 3],
                3: [1, 2]
            }
         -> adjacency matrix = [
                [0, 0, 1, 0]
                [0, 0, 1, 1]
                [1, 1, 0, 1]
                [0, 1, 1, 0]
            ]
    """
    n = len(adjacency_list)
    adjacency_matrix = [[0] * n for _ in range(n)]
    for key, value in adjacency_list.items():
        for node in value:
            adjacency_matrix[key][node] = 1
    for row in adjacency_matrix:
        print(row)
    return adjacency_matrix

adjacency_list_to_matrix({0: [2], 1: [2, 3], 2: [0, 1, 3], 3: [1, 2]})