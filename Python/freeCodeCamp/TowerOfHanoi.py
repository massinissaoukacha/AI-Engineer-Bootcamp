def hanoi_solver(total_disks):
        """
        The hanoi_solver function should solve the puzzle following the given rules in 2^n - 1 moves, where n is the total number of disks.

        The hanoi_solver function should return a string with all the moves taken to solve the puzzle, including the starting arrangement, with each move on a new line. Rods should be represented as lists of integers, (the smallest disk is represented by the number 1) with each rod separated by a space. For example, hanoi_solver(3) should return the following:
        [3, 2, 1] [] []
        [3, 2] [] [1] on commence à dipiler jusqu'à le plus bas element : plus grand
        [3] [2] [1]
        [3] [2, 1] []
        [] [2, 1] [3]
        [1] [2] [3]
        [1] [] [3, 2]
        [] [] [3, 2, 1]
        6. hanoi_solver(4) should return 
        [4, 3, 2, 1] [] []\n[4, 3, 2] [1] []\n[4, 3] [1] [2]\n[4, 3] [] [2, 1]\n
        [4] [3] [2, 1]\n[4, 1] [3] [2]\n[4, 1] [3, 2] []\n[4] [3, 2, 1] []\n[] [3, 2, 1] [4]\n
        [] [3, 2] [4, 1]\n[2] [3] [4, 1]\n[2, 1] [3] [4]\n[2, 1] [] [4, 3]\n[2] [1] [4, 3]\n
        [] [1] [4, 3, 2]\n[] [] [4, 3, 2, 1].
        7. hanoi_solver(5) should return 
        [5, 4, 3, 2, 1] [] []\n[5, 4, 3, 2] [] [1]\n[5, 4, 3] [2] [1]\n[5, 4, 3] [2, 1] []\n
        [5, 4] [2, 1] [3]\n[5, 4, 1] [2] [3]\n[5, 4, 1] [] [3, 2]\n[5, 4] [] [3, 2, 1]\n
        [5] [4] [3, 2, 1]\n[5] [4, 1] [3, 2]\n[5, 2] [4, 1] [3]\n[5, 2, 1] [4] [3]\n
        [5, 2, 1] [4, 3] []\n[5, 2] [4, 3] [1]\n[5] [4, 3, 2] [1]\n[5] [4, 3, 2, 1] []\n
        [] [4, 3, 2, 1] [5]\n[1] [4, 3, 2] [5]\n[1] [4, 3] [5, 2]\n[] [4, 3] [5, 2, 1]\n
        [3] [4] [5, 2, 1]\n[3] [4, 1] [5, 2]\n[3, 2] [4, 1] [5]\n[3, 2, 1] [4] [5]\n
        [3, 2, 1] [] [5, 4]\n[3, 2] [] [5, 4, 1]\n[3] [2] [5, 4, 1]\n[3] [2, 1] [5, 4]\n
        [] [2, 1] [5, 4, 3]\n[1] [2] [5, 4, 3]\n[1] [] [5, 4, 3, 2]\n[] [] [5, 4, 3, 2, 1].
        8. hanoi_solver(n) should solve the tower of Hanoi puzzle for any positive value of n.
        """
        if total_disks == 1:
             return "[1] [] []\n[] [] [1]"
        # Three case : Total_disks < Total_rods = 3 , Total_disks = Total_rods, Total_disks > Total_rods

        # case of Total_disks <= Total_rods = 3
        Rods = [[], [], []]
        Rods[0] = [disk for disk in range(total_disks, 0, -1)]
        first_rod = []
        first_rod.extend(Rods[0])
        print(Rods)
        minimum = min(total_disks, len(Rods))
        impair = total_disks % 2 != 0
        while Rods[-1] != first_rod:
            #1-dépiler jusqu'à le plus bas element
            i =  minimum - 1 if impair else minimum - 2      
            while len(Rods[0]) > 1 and 0 < i < len(Rods):
                #dépiler & empiler dans le plus loin rod disponible, parcours du Rods en inverse de dernier en avant
                Rods[i].append(Rods[0].pop()) # ou bien directement Rods[Rod[0].index(sommet) - total_disk]
                print(Rods)
                i += -1 if impair else 1

            #2-libérer le dernier rod pour empiler le grand disk
            if total_disks >= len(Rods): 
                Rods[-2].append(Rods[-1].pop())
                print(Rods)
            #Empilement du dernier disk jusqu'à le resultat attendu
            for i in range(min(total_disks, len(Rods) -1)):
                if len(Rods[i]) == 1 :
                    Rods[-1].append(Rods[i].pop())
                    print(Rods)
                elif len(Rods[i]) > 1 :
                    #pop & push
                    Rods[i-1].append(Rods[i].pop())
                    print(Rods)
                    if Rods[i][-1] > Rods[i-1][-1]:
                         continue
                    Rods[-1].append(Rods[i].pop())
                    print(Rods)
                    Rods[-1].append(Rods[i-1].pop())
                    print(Rods)
            break
        return Rods

if __name__ == '__main__':
    print(hanoi_solver(4))