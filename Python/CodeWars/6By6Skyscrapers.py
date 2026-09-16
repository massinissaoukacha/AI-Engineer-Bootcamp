def solve_puzzle(clues):
    from itertools import permutations

    N = 6
    nums = tuple(range(1, N + 1))

    # Unpack clues clockwise
    top    = clues[0:6]
    right  = clues[6:12]
    bottom = clues[12:18]
    left   = clues[18:24]

    # Row and column clues (accounting for reversed directions)
    row_left  = [left[5 - r]  for r in range(N)]
    row_right = [right[r]     for r in range(N)]
    col_top    = [top[c]        for c in range(N)]
    col_bottom = [bottom[5 - c] for c in range(N)]

    def visible_count(seq):
        vis, mx = 0, 0
        for h in seq:
            if h > mx:
                mx = h
                vis += 1
        return vis

    def fits_clues(seq, l, r):
        if l and visible_count(seq) != l:
            return False
        if r and visible_count(seq[::-1]) != r:
            return False
        return True

    all_rows = list(permutations(nums))

    # Precompute candidate rows per row index (left/right clues)
    row_candidates = [
        [row for row in all_rows if fits_clues(row, row_left[r], row_right[r])]
        for r in range(N)
    ]

    # Precompute candidate columns per column index (top/bottom clues)
    col_perms = [
        [col for col in all_rows if fits_clues(col, col_top[c], col_bottom[c])]
        for c in range(N)
    ]

    # Domains for columns: lists of indices into col_perms[c] that are currently allowed
    col_domains = [list(range(len(col_perms[c]))) for c in range(N)]

    # Grid rows (None or tuple of 6 ints)
    grid = [None] * N
    unassigned_rows = set(range(N))

    # Helper: compute available values at a specific row position r for each column c,
    # given current column domains.
    def available_values_at_rowpos(r):
        avail = [None] * N
        for c in range(N):
            vals = set()
            cp = col_perms[c]
            for idx in col_domains[c]:
                vals.add(cp[idx][r])
            avail[c] = vals
        return avail

    # Choose next row to assign by MRV w.r.t. current column domains
    def select_row():
        best_r, best_count = None, 10**9
        for r in unassigned_rows:
            avail_vals = available_values_at_rowpos(r)
            # Count row candidates that are compatible with current column domains
            cnt = 0
            for row in row_candidates[r]:
                ok = True
                for c, v in enumerate(row):
                    if v not in avail_vals[c]:
                        ok = False
                        break
                if ok:
                    cnt += 1
                    if cnt >= best_count:
                        break
            if cnt == 0:
                return r, 0  # immediate dead end
            if cnt < best_count:
                best_r, best_count = r, cnt
                if cnt == 1:
                    break
        return best_r, best_count

    # Build compatible row list for a specific row r
    def compatible_rows_for(r):
        avail_vals = available_values_at_rowpos(r)
        comp = []
        for row in row_candidates[r]:
            if all(row[c] in avail_vals[c] for c in range(N)):
                comp.append(row)
        return comp

    # Backtracking with forward-checking over column domains
    def dfs():
        if not unassigned_rows:
            return True  # all rows assigned; column domains already respect top/bottom + uniqueness

        r, count = select_row()
        if count == 0:
            return False

        for row in compatible_rows_for(r):
            # Save state
            saved_domains = [dom[:] for dom in col_domains]

            # Commit row r and filter each column's domain by row value at position r
            grid[r] = row
            unassigned_rows.remove(r)
            feasible = True
            for c, v in enumerate(row):
                dom = col_domains[c]
                if len(dom) != len(saved_domains[c]):
                    # shouldn't happen, but keep consistent with saved copy
                    saved_domains[c] = dom[:]
                filtered = [idx for idx in dom if col_perms[c][idx][r] == v]
                if not filtered:
                    feasible = False
                    break
                col_domains[c] = filtered

            if feasible and dfs():
                return True

            # Undo
            for c in range(N):
                col_domains[c] = saved_domains[c]
            grid[r] = None
            unassigned_rows.add(r)

        return False

    assert dfs(), "No solution found."
    return tuple(tuple(grid[r]) for r in range(N))