def hanoi_solver(total_disks):
    Rods = [list(range(total_disks, 0, -1)), [], []]

    # List to record the string snapshot of each state
    history = []
    def record_state():
        history.append(f'{Rods[0]} {Rods[1]} {Rods[2]}')

    # Record the initial state before any moves are made
    record_state()

    def move(total_disks, source, auxiliary, destination):
        if total_disks == 1:
            destination.append(source.pop())
            record_state()
            return
    
        #step 1: move the n-1 disks from source to auxiliary using destination as helper
        move(total_disks - 1, source, destination, auxiliary)

        #step 2: move the n disk from source to destination
        destination.append(source.pop())
        record_state()

        #step 3: move the n-1 disks from auxiliary to destination
        move(total_disks - 1, auxiliary, source, destination)

    move(total_disks, Rods[0], Rods[1], Rods[2])

    # Return all recorded snapshots joined together with newlines
    return '\n'.join(history)

if __name__ == '__main__':
    print(hanoi_solver(4))