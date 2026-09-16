from typing import List, Tuple, Optional

class MultipleSolutionsError(Exception):
    pass

class UnsolvableSudokuError(Exception):
    pass

def sudoku_solver(grid: List[List[int]]) -> List[List[int]]:
    """
    Solve a 9x9 Sudoku puzzle.

    Input:
      grid: 9x9 list of lists with integers 0..9, where 0 means empty.

    Returns:
      A new 9x9 list of lists containing the solved grid (values 1..9).

    Raises:
      ValueError: if the input grid is invalid (shape/content/duplicate conflicts).
      MultipleSolutionsError: if the puzzle has more than one solution.
      UnsolvableSudokuError: if the puzzle has no solution.
    """
    # Validate input format and initial consistency
    _validate_grid_structure(grid)
    if not _is_consistent(grid):
        raise ValueError("Invalid grid: duplicate conflict in a row, column, or box.")

    # Use bitmasks for fast constraints: for each unit, a 9-bit mask where 1 means the digit is used
    rows = [0] * 9
    cols = [0] * 9
    boxes = [0] * 9

    empties = []
    for r in range(9):
        for c in range(9):
            v = grid[r][c]
            if v == 0:
                empties.append((r, c))
            else:
                bit = 1 << (v - 1)
                b = (r // 3) * 3 + (c // 3)
                if (rows[r] & bit) or (cols[c] & bit) or (boxes[b] & bit):
                    raise ValueError("Invalid grid: duplicate conflict in a row, column, or box.")
                rows[r] |= bit
                cols[c] |= bit
                boxes[b] |= bit

    # Work on a copy to avoid mutating the caller's grid
    board = [row[:] for row in grid]

    # Prepare a place to store up to 2 solutions
    solutions = []

    def candidates(r: int, c: int) -> int:
        """Return bitmask of available candidates for cell (r,c)."""
        b = (r // 3) * 3 + (c // 3)
        used = rows[r] | cols[c] | boxes[b]
        return (~used) & 0x1FF  # 9 bits

    def set_cell(r: int, c: int, val: int):
        """Place val at (r,c) and update masks."""
        board[r][c] = val
        bit = 1 << (val - 1)
        rows[r] |= bit
        cols[c] |= bit
        boxes[(r // 3) * 3 + (c // 3)] |= bit

    def unset_cell(r: int, c: int, val: int):
        """Remove val from (r,c) and update masks."""
        board[r][c] = 0
        bit = 1 << (val - 1)
        rows[r] ^= bit
        cols[c] ^= bit
        boxes[(r // 3) * 3 + (c // 3)] ^= bit

    def propagate_singles(stack: List[Tuple[int,int]]) -> Optional[List[Tuple[int,int,int]]]:
        """
        Deterministically fill all naked singles.
        Returns a log of assignments [(r,c,val), ...] to allow undo on backtrack.
        If a contradiction is found, return None.
        """
        log = []
        while True:
            progressed = False
            if stack:
                # start from provided cells; else scan all empties
                to_check = stack
                stack = []
            else:
                to_check = [(r, c) for r in range(9) for c in range(9) if board[r][c] == 0]

            for r, c in to_check:
                if board[r][c] != 0:
                    continue
                mask = candidates(r, c)
                if mask == 0:
                    # no candidates -> contradiction
                    for rr, cc, vv in reversed(log):
                        unset_cell(rr, cc, vv)
                    return None
                # if exactly one bit set => naked single
                if mask & (mask - 1) == 0:
                    val = (mask.bit_length() - 1) + 1
                    set_cell(r, c, val)
                    log.append((r, c, val))
                    progressed = True
                    # adding neighbors to check further propagation is optional; scanning all is fine
            if not progressed:
                break
        return log

    def choose_mrv_cell() -> Optional[Tuple[int, int, int]]:
        """
        Choose the empty cell with the fewest candidates (MRV).
        Returns (r, c, candidates_mask) or None if solved.
        """
        best = None
        best_count = 10
        best_mask = 0
        for r in range(9):
            for c in range(9):
                if board[r][c] != 0:
                    continue
                mask = candidates(r, c)
                cnt = mask.bit_count()
                if cnt == 0:
                    return (r, c, 0)  # dead end
                if cnt < best_count:
                    best = (r, c)
                    best_count = cnt
                    best_mask = mask
                    if cnt == 1:
                        return (r, c, mask)
        if best is None:
            return None
        return (best[0], best[1], best_mask)

    def search():
        # Early propagation
        log = propagate_singles(stack=[])
        if log is None:
            return  # contradiction

        choice = choose_mrv_cell()
        if choice is None:
            # Solved
            solutions.append([row[:] for row in board])
            # Undo propagation before returning to explore potential second solution
            for r, c, v in reversed(log):
                unset_cell(r, c, v)
            return

        r, c, mask = choice
        if mask == 0:
            # Dead end
            for rr, cc, vv in reversed(log):
                unset_cell(rr, cc, vv)
            return

        # Try candidates in ascending order
        m = mask
        while m:
            bit = m & -m
            val = (bit.bit_length() - 1) + 1
            set_cell(r, c, val)
            # Local propagation starting from this cell may speed up
            log2 = propagate_singles(stack=[(r, c)])
            if log2 is not None:
                search()
                # undo local propagation
                for rr, cc, vv in reversed(log2):
                    unset_cell(rr, cc, vv)
            unset_cell(r, c, val)

            if len(solutions) > 1:
                # Found at least two solutions; we can stop early
                break
            m ^= bit

        # Undo initial propagation for this frame
        for rr, cc, vv in reversed(log):
            unset_cell(rr, cc, vv)

    # Kick off the search
    search()

    if len(solutions) == 0:
        raise UnsolvableSudokuError("No solution exists for the given puzzle.")
    if len(solutions) > 1:
        raise MultipleSolutionsError("The puzzle has multiple solutions.")
    return solutions[0]


def _validate_grid_structure(grid: List[List[int]]):
    if not isinstance(grid, list) or len(grid) != 9:
        raise ValueError("Grid must be a 9x9 list of lists.")
    for i, row in enumerate(grid):
        if not isinstance(row, list) or len(row) != 9:
            raise ValueError(f"Row {i} must be a list of length 9.")
        for j, v in enumerate(row):
            if not isinstance(v, int):
                raise ValueError(f"Cell ({i},{j}) must be an integer 0..9.")
            if v < 0 or v > 9:
                raise ValueError(f"Cell ({i},{j}) has value {v}, expected 0..9.")


def _is_consistent(grid: List[List[int]]) -> bool:
    """Check there are no duplicate digits in any row, column, or box (ignoring zeros)."""
    # rows
    for r in range(9):
        seen = set()
        for c in range(9):
            v = grid[r][c]
            if v == 0:
                continue
            if v in seen:
                return False
            seen.add(v)
    # cols
    for c in range(9):
        seen = set()
        for r in range(9):
            v = grid[r][c]
            if v == 0:
                continue
            if v in seen:
                return False
            seen.add(v)
    # boxes
    for br in range(0, 9, 3):
        for bc in range(0, 9, 3):
            seen = set()
            for dr in range(3):
                for dc in range(3):
                    v = grid[br + dr][bc + dc]
                    if v == 0:
                        continue
                    if v in seen:
                        return False
                    seen.add(v)
    return True

#Quick example:

puzzle = [
    [0,0,0, 2,6,0, 7,0,1],
    [6,8,0, 0,7,0, 0,9,0],
    [1,9,0, 0,0,4, 5,0,0],

    [8,2,0, 1,0,0, 0,4,0],
    [0,0,4, 6,0,2, 9,0,0],
    [0,5,0, 0,0,3, 0,2,8],

    [0,0,9, 3,0,0, 0,7,4],
    [0,4,0, 0,5,0, 0,3,6],
    [7,0,3, 0,1,8, 0,0,0],
]
solution = sudoku_solver(puzzle)
for row in solution:
    print(row)