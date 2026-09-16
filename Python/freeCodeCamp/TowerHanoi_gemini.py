def hanoi_solver(n):
    # Initialize the three rods: 
    # Rod 0 gets all disks from largest to smallest, Rod 1 and 2 start empty.
    rods = [list(range(n, 0, -1)), [], []]
    
    # List to record the string snapshot of each state
    history = []
    
    # Helper function to append a formatted string snapshot of the current state
    def record_state():
        history.append(f"{rods[0]} {rods[1]} {rods[2]}")

    # Record the initial state before any moves are made
    record_state()

    # Recursive function to handle the movements
    def move(disks, source, auxiliary, target):
        if disks == 1:
            # Base case: Move the single disk directly
            rods[target].append(rods[source].pop())
            record_state()
            return
        
        # 1. Move top n-1 disks from source to auxiliary using target as a helper
        move(disks - 1, source, target, auxiliary)
        
        # 2. Move the largest remaining disk from source to target
        rods[target].append(rods[source].pop())
        record_state()
        
        # 3. Move the n-1 disks from auxiliary back to target using source as a helper
        move(disks - 1, auxiliary, source, target)

    # Initiate the recursive solution moving n disks from Rod 0 to Rod 2 using Rod 1
    move(n, 0, 1, 2)
    
    # Return all recorded snapshots joined together with newlines
    return "\n".join(history)

# Example usage:
if __name__ == "__main__":
    print(hanoi_solver(3))