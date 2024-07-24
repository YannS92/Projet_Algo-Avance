import numpy as np
import time
import matplotlib.pyplot as plt
import timeit
import random

nb_villes=200 #Nombre de villes à générer
tempsMax=200 #Temps (Distance) max séparant 2 villes


def generer_matrice_adjacence(taille,typeDeGraphe):
    matrice = np.empty((taille, taille))              
    if(typeDeGraphe == 'Complete'):               
        for i in range(taille):
            for j in range(i,taille):
                valeur = 1 if i!=j else 0 
                matrice[i][j] = valeur
                matrice[j][i] = valeur
    else:
         for i in range(taille):
            for j in range(i,taille):
                valeur = random.randint(0, 1)  if i!=j else 0
                matrice[i][j] = valeur
                matrice[i][j] = valeur
    return matrice
    

matriceAdjacence = generer_matrice_adjacence(nb_villes, "Complete")
print(matriceAdjacence)

def generer_matrice_pondere(matrice):
    for i in range(len(matrice)):
        for j in range(i,len(matrice)):
            if(matrice[i][j] != 0):
                valeur = random.randint(0, tempsMax)
                matrice[i][j] = valeur
                matrice[j][i] = valeur
    return matrice



start = time.time() #Commence le calcul du temps d'exécution
graphe = generer_matrice_pondere(matriceAdjacence) ##Génère une matrice pour n villes et avec un temps maximum
print(graphe)
stop = time.time() #Stop le calcul du temps d'exécution

print("\nTemps total d'exécution: " + str(stop-start) + " secondes")

#Génère les voisins valides d'une solution
def getNeighbors(path, graphe):
    startNode=path.pop(0) #Réinitialisation du point de départ
    path.pop(len(path)-1) #Réinitialisation du point d'arrivé
    index=0
    for i in range(len(path)):
        for j in range(1,len(path)-i):
            neighborPath=path.copy() #On fait une copie du chemin fourni
            neighborPath[i], neighborPath[i+j] = neighborPath[i+j], neighborPath[i] #Swap des voisins
            neighborPath.insert(0,startNode) #Ajout du point de départ
            neighborPath.append(startNode) #Ajout du point d'arrivé
            yield(neighborPath)

# Test de la fonction
for voisin in getNeighbors([0,1,2,3,0],graphe):
    print(voisin)


#Renvoi le temps total d'un chemin
def getPathTime(path, graphe):
    time=0 #Initialisation du temps
    for i in range(len(path)-1):
        time+=graphe[path[i]][path[i+1]] #On ajoute le temps 
    return time

#Donne l'indice de la ville de plus proche de la ville actuelle non-visitée
def nextCity(currentCityPosition,visitedCitiesPosition,graphe) :
    mini = 1000000000
    minimumPosition = -1
    for i in range(len(graphe)) :
        if visitedCitiesPosition[i] == False : #Index de la ville dans la liste des villes visitées
            if graphe[currentCityPosition][i] < mini : #Si l'index de la ville actuelle est inférieur à mini
                mini = graphe[currentCityPosition][i] #On récupère l'index de la ville actuelle
                minimumPosition = i #On récupère le numéro dans graphe de la ville
    return minimumPosition


#Donne le chemin à suivre du voyageur de commerce sous forme de tableau d'indice
def nearestNeighbor(startCity,graphe):
    visitedCitiesPosition = [False] * len(graphe) #Pas de villes visitées au début
    path = [0]* (len(graphe)) #Le chemin est vide

    currentCityPosition = startCity #Indice de la ville de départ
    visitedCitiesPosition[currentCityPosition] = True # On dit que la ville est visitée.
    path[0] = currentCityPosition

    for i in range(1,len(graphe)) :
        indiceNextCity= nextCity(currentCityPosition,visitedCitiesPosition,graphe)
        path[i] = indiceNextCity
        currentCityPosition = indiceNextCity
        visitedCitiesPosition[currentCityPosition] = True # La ville est visitée elle ne peut plus être prise.
    path.append(path[0])
    return path

reNearestNeighbor=nearestNeighbor(0,graphe)

print("\nChemin avec l'algorithme du plus proche voisin : " + str(reNearestNeighbor))
print("")
print("Valeur de ce chemin : " + str(getPathTime(reNearestNeighbor,graphe)))
def tabuSearch(startNode, tabuLength, iterMax, graphe, withNearestNeighbor):
    """
    1. On part d'un element de notre ensemble de recherche qu'on declare element courant
    2. On considere le voisinage de l'element courant et on choisit le  meilleur d'entre
       eux comme nouvel element courant, parmi ceux absents de la liste tabou, et on l'ajoute
       a la liste tabou
    3. On boucle jusqu'a condition de sortie.
    """

    nbIter = 0
    tabuList = list()

    # Ici on utilise comme chemin initiale le résultat de notre algorithme du plus proche voisin
    if withNearestNeighbor==True:
        initialElement=nearestNeighbor(startNode,graphe)
    #On peut également utiliser un chemin initial aléatoire, pour cela, il faut décommenter les 2 lignes ci dessous et commenter la ligne du dessus
    else:
        initialElement=[i for i in range(len(graphe))]
        initialElement.remove(startNode)
        initialElement.append(startNode)
        initialElement.insert(0,startNode)
        
    # variables solutions pour la recherche du voisin optimal non tabou
    currentElement = initialElement
    bestNeighbor=currentElement
    bestNeighborGlobal=currentElement

    # variables valeurs pour la recherche du voisin optimal non tabou
    bestCost=100000
    bestCostGlobal=100000

    # variables pour l'affichage
    nbTabou=0
    bestGlobalFound=0
    
    # liste des solutions courantes et des meilleures trouvées, pour afficher la trajectoire
    paths=list()
    bestPaths=list()
    
    while (nbIter<iterMax):
        nbIter += 1       
        bestCost=100000

        # on parcours tous les voisins de la solution courante
        for neighbor in getNeighbors(currentElement,graphe):
            if getPathTime(neighbor,graphe) < bestCost:
                if neighbor not in tabuList:
                    bestCost = getPathTime(neighbor,graphe)
                    bestNeighbor = neighbor
          
        # on met a jour la meilleure solution rencontree depuis le debut
        if bestCost<bestCostGlobal:
            bestGlobalFound+=1
            bestNeighborGlobal=bestNeighbor
            bestCostGlobal=bestCost
            #print("Meilleur global trouvé ! : " + str(bestNeighborGlobal) + " avec une valeur de :" + str(bestCostGlobal))
      
        bestPaths.append(bestCostGlobal)
        
        # on passe au meilleur voisin non tabou trouve     
        currentElement=bestNeighbor.copy()
        paths.append(bestCost)
        
        # on met a jour la liste tabou
        tabuList.append(bestNeighbor)

        # on supprime la solution la plus ancienne si la liste tabou à atteint sa taille maximale
        if len(tabuList) > tabuLength:
            del tabuList[0]

    # On insère à l'élément initiale la ville d'origine
    initialElement.insert(0,startNode)
    initialElement.append(startNode)
    return bestNeighborGlobal, paths, bestPaths, initialElement


#------------------ Execution de l'algorithme ---------------------

# Paramètres de génération du graphe
nbVilles=100
tempsMax=200

graphe = generer_matrice_pondere(matriceAdjacence)

# Modifier ce paramètre pour modifier le nombre d'itération maximum de la recherche tabou
iterMaximum=500
# Modifier ce paramètre pour modifier la taille maximum de la liste tabou
tabuMax=len(graphe)
# Modifier ce paramètre pour activer ou non l'utilisation du plus proche voisin comme chemin initial
useNearestNeighbor=True
# Modifier ce paramètre pour changer la ville de départ
departureCity=0

startTime = time.time()
sol, paths, bestPaths, initialPath=tabuSearch(startNode=departureCity, tabuLength=tabuMax, iterMax=iterMaximum, graphe=graphe, withNearestNeighbor=useNearestNeighbor)
execTime = (time.time() - startTime)

print("La valeur du chemin initial est :",str(getPathTime(initialPath,graphe)))
print("\n---------------------------------------------")
#print("\nLe meilleur chemin trouvé est : " + str(resNearestNeighbor(sol)))
print("\nSa valeur est de : " + str(getPathTime(sol,graphe)) + " mn, soit " + str("{:.2f}".format(getPathTime(sol,graphe)/60)) + " h")
print("\nTemps d'execution : " + str(execTime) + " secondes\n\n")

# Affichage des résultats sur le graphique
plt.xlabel("Nombre d'itérations", fontsize=16)
plt.ylabel("Valeur de solution", fontsize=16)

res = plt.plot(range(iterMaximum), paths,label='Meilleure valeur pour chaque itération')
res = plt.plot(range(iterMaximum), bestPaths,label='Meilleure valeur globale')

plt.legend()
font2 = {'size':14}
plt.title("\nExploration de la zone de recherche par notre algorithme\n", loc = 'center',fontdict = font2)
