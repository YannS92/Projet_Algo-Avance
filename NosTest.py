from collections import deque
import copy
import numpy as np
import random
from itertools import product, combinations
'''
matrix_zone_A = [
    [0,1,0,1,0,0,0,0,0,0,0],
    [1,0,0,0,1,0,0,0,0,0,0],
    [0,0,0,1,0,0,0,1,0,0,0],
    [1,0,1,0,1,0,0,0,1,0,0],
    [0,1,0,1,0,1,0,0,0,0,0],
    [0,0,0,0,1,0,0,0,0,0,1],
    [0,0,0,0,0,0,0,1,0,1,0],
    [0,0,1,0,1,0,1,0,1,0,0],
    [0,0,0,1,0,0,0,1,0,0,0],
    [0,0,0,0,0,0,1,0,0,0,1],
    [0,0,0,0,0,1,0,0,0,1,0]]

def degreSommetGrapheMatrice(matrice, sommet):
    degre = sum(matrice[sommet])
    return degre

def voisinsSommetGrapheMatrice(matrice, sommet):
    liste = matrice[sommet]
    voisins = []
    for i in range(len(liste)):
        if liste[i] == 1:
            voisins.append(i)
            
    return voisins


def cycleEulerien(matrice):
    # la matrice est passée par référence, on fait donc une copie de la matrice pour éviter d'écraser ses données.
    # comme il faut aussi copier les listes internes, on fait une _copie profonde_
    matrice = copy.deepcopy(matrice)
    n = len(matrice) 

    cycle = deque() # cycle est le cycle à construire
    stack = deque() # stack est la pile de sommets à traiter
    cur = 0         # cur est le sommet courant. on commence avec le premier sommet de la matrice

    # on boucle tant qu'il y a des sommets à traiter dans la pile
    # ou que le sommet courant possède au moins 1 voisin non traité
    while(len(stack) > 0 or degreSommetGrapheMatrice(matrice, cur) != 0): 
          
        # si le sommet courant ne possède aucun voisin, on l'ajoute au cycle
        # et on revient au sommet ajouté précédemment dans la pile (backtracking) 
        # qui devient le nouveau sommet courant
        if degreSommetGrapheMatrice(matrice, cur) == 0:
            cycle.append(cur)
            cur = stack[-1]
            stack.pop()
        #À COMPLÉTER
  
        # si il a au moins 1 voisin, on l'ajoute à la stack pour y revenir plus tard (backtracking)
        # on retire l'arête qu'il partage avec ce voisin, qui devient le sommet courant
        else: 
            for i in range(n):                              
                #À COMPLÉTER
                if matrice[cur][i] > 0:
                    stack.append(cur)
                    matrice[cur][i]=matrice[cur][i]-1
                    matrice[i][cur]=matrice[cur][i]-1
                    cur = i
                    break                                       
    return cycle;

print("### Calcul d'un cycle Eulérien du graphe de la Zone A ###")
cycle = cycleEulerien(matrix_zone_A)
for sommet in cycle: 
    print(sommet+1, "-> ", end = '') 
print(cycle[0]+1)

liste=[0.31,0.32,0.33]
print(max(liste))
print(min(liste))

def bestGrapheEulerien(taille):
    # on génère une matrice aléatoire booléenne (pour pouvoir faire des `ou`)
    # on renvoie la matrice de booléens convertie en matrice d'entiers
    b = np.random.choice((True, False), size=(taille,taille), p=[0.1, 0.9])
    
    # on fait le `ou` logique de la matrice et de sa transposée
    b_symm = np.logical_or(b, b.T)
    
    # on renvoie la matrice de booléens convertie en matrice d'entiers
    return b_symm.astype(int)
print(bestGrapheEulerien(10))

def random_graph(n, p, *, directed=False):
    nodes = range(n)
    adj_list = [[] for i in nodes]
    adj_dic ={}
    possible_edges =  combinations(nodes, 2)
    print(possible_edges)
    for u, v in possible_edges:
        if random.random() < p:
            adj_list[u].append(v+1)

            adj_list[v].append(u+1)
    for i in range(len(adj_list)):
        adj_dic[i+1]=adj_list[i]
    return adj_dic
print(random_graph(3,0.7))


liste={1:[1,1],2:[2,3,5,5]}
liste[1].remove(1)
print(liste)

'''

class Graph():
    def __init__(self, vertices):
        self.graph = [[0 for column in range(vertices)]
                            for row in range(vertices)]
        self.V = vertices
 
    ''' Check if this vertex is an adjacent vertex
        of the previously added vertex and is not
        included in the path earlier '''
    def isSafe(self, v, pos, path):
        # Check if current vertex and last vertex
        # in path are adjacent
        if self.graph[ path[pos-1] ][v] == 0:
            return False
 
        # Check if current vertex not already in path
        for vertex in path:
            if vertex == v:
                return False
 
        return True
 
    # A recursive utility function to solve
    # hamiltonian cycle problem
    def hamCycleUtil(self, path, pos):
 
        # base case: if all vertices are
        # included in the path
        if pos == self.V:
            # Last vertex must be adjacent to the
            # first vertex in path to make a cycle
            if self.graph[ path[pos-1] ][ path[0] ] == 1:
                return True
            else:
                return False
 
        # Try different vertices as a next candidate
        # in Hamiltonian Cycle. We don't try for 0 as
        # we included 0 as starting point in hamCycle()
        for v in range(1,self.V):
 
            if self.isSafe(v, pos, path) == True:
 
                path[pos] = v
 
                if self.hamCycleUtil(path, pos+1) == True:
                    return True
 
                # Remove current vertex if it doesn't
                # lead to a solution
                path[pos] = -1
 
        return False
 
    def hamCycle(self):
        path = [-1] * self.V
 
        ''' Let us put vertex 0 as the first vertex
            in the path. If there is a Hamiltonian Cycle,
            then the path can be started from any point
            of the cycle as the graph is undirected '''
        path[0] = 0
 
        if self.hamCycleUtil(path,1) == False:
            print ("Solution does not exist\n")
            return False
 
        self.printSolution(path)
        return True
 
    def printSolution(self, path):
        print ("Solution Exists: Following",
                 "is one Hamiltonian Cycle")
        for vertex in path:
            print (vertex, end = " ")
        print (path[0], "\n")
 
# Driver Code
 
''' Let us create the following graph
    (0)--(1)--(2)
    | / \ |
    | / \ |
    | /     \ |
    (3)-------(4) '''
g1 = Graph(5)
g1.graph = [ [0, 1, 0, 1, 0], [1, 0, 1, 1, 1],
            [0, 1, 0, 0, 1,],[1, 1, 0, 0, 1],
            [0, 1, 1, 1, 0], ]
 
# Print the solution
g1.hamCycle();
 
''' Let us create the following graph
    (0)--(1)--(2)
    | / \ |
    | / \ |
    | /     \ |
    (3)     (4) '''
g2 = Graph(5)
g2.graph = [ [0, 1, 0, 1, 0], [1, 0, 1, 1, 1],
        [0, 1, 0, 0, 1,], [1, 1, 0, 0, 1],
        [0, 1, 1, 1, 0], ]
 
# Print the solution
g2.hamCycle();
 
# This code is contributed by Divyanshu Mehta 