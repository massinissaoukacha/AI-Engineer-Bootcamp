def dfs_n_queens(n):
    if n < 1:
        return []
    
    cols = set()
    diag1 = set()  # row - col
    diag2 = set()  # row + col
    solutions = []
    current = []   # stores column index for each row

    def backtrack(row):
        if row == n:
            solutions.append(current.copy())
            return
        
        for col in range(n):
            if col in cols or (row - col) in diag1 or (row + col) in diag2:
                continue
            
            # Place the queen
            cols.add(col)
            diag1.add(row - col)
            diag2.add(row + col)
            current.append(col)
            
            # Move to next row
            backtrack(row + 1)
            
            # Remove the queen (backtrack)
            cols.remove(col)
            diag1.remove(row - col)
            diag2.remove(row + col)
            current.pop()

    backtrack(0)
    return solutions
