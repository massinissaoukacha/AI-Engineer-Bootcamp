
#from ...nombre_to_ordinal import nombre_vers_ordinal
from pathlib import Path
import sys
sys.path.append(str(Path(__file__).resolve().parent.parent.parent))
from nombre_to_ordinal import nombre_vers_ordinal
import numpy as np
import pandas as pd


class GraphObject:
    def __init__(self, type, NbrSommets, NbrArcs):
        self.type = type
        self.NbrSommets = NbrSommets
        self.NbrArcs = NbrArcs
        self.sommets = [str(input(f"entrer {nombre_vers_ordinal(i)} sommet :")) for i in range(1,self.NbrSommets+1)]
        self.arcs = [
            (
                str(input(f"({nombre_vers_ordinal(i)} Arc) entrer 1er sommet:")),
                str(input(f"({nombre_vers_ordinal(i)} Arc) entrer 2nd sommet:"))
            ) 
            for i in range(1,self.NbrArcs+1)
        ]
        self.matrix = pd.DataFrame(
            np.zeros((self.NbrSommets, self.NbrSommets), dtype=int),
            index= self.sommets,
            columns= self.sommets
        )
       
    def MatriceAdjacence(self):
        for arc in self.arcs:
            self.matrix.loc[arc[0], arc[1]] = 1
            self.matrix.loc[arc[1], arc[0]] = 1
        return self.matrix
