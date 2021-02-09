from scipy.spatial.distance import pdist, squareform
from visualize import plot
import matplotlib.pyplot as plt
import numpy as np
import random
import math
import sys
import copy
import math
import time
from math import hypot

#grid searhc


MUTATION_RATE_DELETE = 5
MUTATION_RATE_POINT = 80
MUTATION_RATE_MOVE_POINT = 100
MUTATION_MOVE_SIZE = 1
FACTOR_INCREASE = 100





cityCoordinates = [[50,00],[30,20],[80,20]]
np.random.uniform(0,100, size=(5,2))
#[[0,1],[0,2],[0,3]]

#cityCoordinates = cityCoordinates.tolist()
obstacles=[]


class Genome():
    path = []
    chromosomes = []
    fitness = 9999.999
    squaredistances = [[]]


def getPoints():
    return cityCoordinates


def CreateNewPopulation(size):
    population = []
    genome = Genome()
    genome.chromosomes = cityCoordinates
    a = squareform(createdistances(cityCoordinates))
    genome.squaredistances = a.tolist()
    firstPath = prim(genome)
    for x in range(size):
        newGenome = Genome()
        newGenome = copy.deepcopy(firstPath)
        population.append(newGenome)
    return population

def createdistances(array):
    distances = []
    for x in range(len(array)-1):
        for y in range(x+1,len(array)):
            distances.append(hypot(array[x][0]-array[y][0], array[x][1]-array[y][1]))
    return distances

def updatesquarearray(oldarray, chromosomes, pointpos):
    if (len(chromosomes) > len(oldarray)):
        array = [0 for col in range(len(chromosomes)-1)]
        oldarray.append(array)
        for x in range(len(chromosomes)):
            oldarray[x].append(0)
    print(oldarray,pointpos)
    for x in range(len(chromosomes)):    
        calc = hypot(chromosomes[x][0]-chromosomes[pointpos][0], chromosomes[x][1]-chromosomes[pointpos][1])
        oldarray[x][pointpos] = calc
        oldarray[pointpos][x] = calc
    return oldarray
 
def deletesquarearray(oldarray,pointpos):
    temp = oldarray.copy()
    for x in range(len(oldarray)):
        temp[x].pop(pointpos)

    del temp[pointpos]
    return temp.copy()



def collide(p1,p2):
    for x in range(len(obstacles)-1):
        if(x == 0):
            if(doIntersect(p1,p2,obstacles[len(obstacles)-1],obstacles[0])):
                return True
        if(doIntersect(p1,p2,obstacles[x],obstacles[x+1])):
                return True
    return False
    

def onSegment(p, q, r): 
	if ( (q[0] <= max(p[0], r[0])) and (q[0] >= min(p[0], r[0])) and
		(q[1] <= max(p[1], r[1])) and (q[1]>= min(p[1], r[1]))): 
		return True
	return False

def orientation(p, q, r): 
	val = (float(q[1] - p[1]) * (r[0] - q[0])) - (float(q[0] - p[0]) * (r[1] - q[1])) 
	if (val > 0): 
		# Clockwise orientation 
		return 1
	elif (val < 0): 
		# Counterclockwise orientation 
		return 2
	else: 
		# Colinear orientation 
		return 0

def doIntersect(p1,q1,p2,q2): 
	o1 = orientation(p1, q1, p2) 
	o2 = orientation(p1, q1, q2) 
	o3 = orientation(p2, q2, p1) 
	o4 = orientation(p2, q2, q1) 
	if ((o1 != o2) and (o3 != o4)): 
		return True
	if ((o1 == 0) and onSegment(p1, p2, q1)): 
		return True
	if ((o2 == 0) and onSegment(p1, q2, q1)): 
		return True
	if ((o3 == 0) and onSegment(p2, p1, q2)): 
		return True
	if ((o4 == 0) and onSegment(p2, q1, q2)): 
		return True
	return False



def prim(genome):
    MST = Genome()
    MST.chromosomes = genome.chromosomes.copy()
    G = genome.squaredistances.copy()
    MST.squaredistances = G.copy()
    MST.fitness = 0
    path = []
    
    INF = sys.maxsize
    V = len(G[0])
    selected = []
    for a in range(V):
        selected.append(0)
    no_edge = 0
    selected[0] = True
    
    while (no_edge < V - 1):
        minimum = INF
        x = 0
        y = 0
        for i in range(V):
            if selected[i]:
                for j in range(V):
                    if ((not selected[j]) and G[i][j]):  
                        # not in selected and there is an edge
                        if minimum > G[i][j]:
                            minimum = G[i][j]
                            x = i
                            y = j
        path.append([x,y])
        MST.fitness += float(G[x][y])
        selected[y] = True
        no_edge += 1
        MST.path = path.copy()
    return MST






def mutatePopulation(population,generation,mutationrateadd,mutationrateremove,mutationratemove):
    unmutated = 0
    for genome in population:
        #if(unmutated > 1):
            if (random.randrange(0, 100) < mutationrateadd) or (len(genome.chromosomes) == len(cityCoordinates)):
                genome.chromosomes.append([np.random.uniform(0,100),np.random.uniform(0,100)])
                genome.squaredistances = updatesquarearray(genome.squaredistances,genome.chromosomes,len(genome.chromosomes)-1).copy()
    
            if (random.randrange(0,100) < mutationratemove):
                pointindex = np.random.randint(len(cityCoordinates),len(genome.chromosomes))
                angle = np.random.uniform(0,360)
                genome.chromosomes[pointindex][0] = genome.chromosomes[pointindex][0] + MUTATION_MOVE_SIZE*math.sin(math.radians(angle))
                genome.chromosomes[pointindex][1] = genome.chromosomes[pointindex][1] + MUTATION_MOVE_SIZE*math.cos(math.radians(angle))
                genome.squaredistances = updatesquarearray(genome.squaredistances,genome.chromosomes,pointindex)

            if (random.randrange(0,100) < mutationrateremove) or (generation == 0) or True:
                fit = prim(genome).fitness
                size = len(genome.chromosomes)-1
                current = Genome()
                while(size >= len(cityCoordinates)):
                    current.squaredistances = deletesquarearray(genome.squaredistances,size).copy()
                    current.chromosomes = genome.chromosomes.copy()
                    del current.chromosomes[size]
                    if(fit>=prim(current).fitness):
                        genome.chromosomes = current.chromosomes.copy()
                        genome.squaredistances = current.squaredistances.copy()
                    size -=1
        
            temp = prim(genome)
            genome.path = temp.path.copy()
            genome.fitness = temp.fitness

          


        #unmutated +=1  

    

def naturalSelection(population,popSize):
    count = 0
    for genome in population:
        population[popSize-1-count] = copy.deepcopy(genome)
        count += 1



def findBestGenome(population):
    allFitness = [i.fitness for i in population]
    bestFitness = min(allFitness)
    return population[allFitness.index(bestFitness)]


def GeneticAlgorithm(popSize, maxGeneration,points):
    global obstacles
    obstacles = points
    start = time.perf_counter()
    generation = 0
    population = CreateNewPopulation(popSize)
    startingGenome = prim(population[0]) 
    leadingFitnesses= []
    leadingGenome = Genome()
    bestGenome = Genome()
    while generation < maxGeneration:
        generation += 1
        population.sort(key=lambda x: x.fitness, reverse=False)
        naturalSelection(population,popSize)
        mutatePopulation(population,maxGeneration-generation,MUTATION_RATE_POINT,MUTATION_RATE_DELETE,MUTATION_RATE_MOVE_POINT)
        leadingGenome = copy.copy(findBestGenome(population)) 
        leadingFitnesses.append(leadingGenome.fitness)
        average_fitness = round(np.sum([genom.fitness for genom in population]) / len(population), 2)
        if(leadingGenome.fitness<=bestGenome.fitness):
            bestGenome = copy.copy(leadingGenome)
        print("Generation: {0}\t\t Max Generation: {1}\nPopulation Size: {2}\t Average Fitness: {3}\nBest Fitness: {4}\n\n\n"
            .format(generation, maxGeneration, len(population), average_fitness, bestGenome.fitness))

    print(bestGenome.chromosomes,bestGenome.fitness,bestGenome.path,bestGenome.squaredistances)
    plot(int(time.perf_counter()-start),generation, leadingFitnesses,bestGenome, startingGenome,obstacles)

    