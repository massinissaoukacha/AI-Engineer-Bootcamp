from MatriceAdjacence import GraphObject

GRAPHETYPE = "Entrer le type de graphe :"
NOMBRESOMMETS = "Entrer le nombre de sommets :"
NOMBREARCS = "Entrer le nombre des arcs :"
graph = GraphObject(input(GRAPHETYPE), int(input(NOMBRESOMMETS)), int(input(NOMBREARCS)))
m = graph.MatriceAdjacence()
print(m)
