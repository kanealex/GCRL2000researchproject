from scipy.spatial.distance import pdist, squareform
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





cityCoordinates = [[]]
obstacles=[]
generation = 0
maxGeneration = 0


class Genome():
    path = []
    chromosomes = []
    fitness = sys.maxsize

class Generation():
    timer = 0 
    leadingFitnesses = []
    bestGenome = Genome()




def getPoints():
    return cityCoordinates


def CreateNewPopulation(size):
    population = []
    firstPath = prim(cityCoordinates)
    for x in range(size):
        newGenome = Genome()
        newGenome = copy.deepcopy(firstPath)
        population.append(newGenome)
    return population

def createdistances(array):
    distances = []
    for x in range(len(array)-1):
        for y in range(x+1,len(array)):
            factor = 0
            if(collide(array[x],array[y])):
                factor = updatefactor()
            distances.append(factor+(hypot(array[x][0]-array[y][0], array[x][1]-array[y][1])))
    return distances


def updatefactor():
    a = (generation/maxGeneration)*FACTOR_INCREASE
    return a





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



def prim(chro):
    MST = Genome()
    MST.chromosomes = chro
    MST.fitness = 0
    path = []
    G = squareform(createdistances(chro))
    INF = sys.maxsize
    V = G[0].size
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
        MST.path = path
    return MST

def NewPointMutation(genome):
    newPoint = [[np.random.uniform(0,100),np.random.uniform(0,100)]]
    for x in genome.chromosomes:
        newPoint.append(x)
    return prim(newPoint)

def RemovePointMutation(genome):
    mutatedindex = len(genome.chromosomes)-(len(cityCoordinates)+1)
    index = 0
    for i in range(0,mutatedindex):
        if(len(genome.chromosomes) > len(cityCoordinates)+1):
            temp = genome.chromosomes.copy()
            del temp[i-index]
            if(prim(temp).fitness < genome.fitness):
                #print("deleted: {0}".format(genome.chromosomes[i-index]))
                del genome.chromosomes[i-index]
                index += 1

    return prim(genome.chromosomes)


def mutatePopulation(population,generation,mutationrateadd,mutationrateremove,mutationratemove):
    unmutated = 0
    for genome in population:
        if(unmutated > 1):
            if (random.randrange(0, 100) < mutationrateadd) or (len(genome.chromosomes) == len(cityCoordinates)):
                newPoint = [[np.random.uniform(0,100),np.random.uniform(0,100)]]
                for x in genome.chromosomes:
                    newPoint.append(x)
                genome.chromosomes = newPoint.copy()
            if (random.randrange(0,100) < mutationratemove):
                pointindex = np.random.randint(0,len(genome.chromosomes) - (len(cityCoordinates)))
                angle = np.random.uniform(0,360)
                genome.chromosomes[pointindex][0] = genome.chromosomes[pointindex][0] + MUTATION_MOVE_SIZE*math.sin(math.radians(angle))
                genome.chromosomes[pointindex][1] = genome.chromosomes[pointindex][1] + MUTATION_MOVE_SIZE*math.cos(math.radians(angle))
            if ((random.randrange(0,100) < mutationrateremove) or (generation == 0)):
                fit = prim(genome.chromosomes).fitness
                size = (len(genome.chromosomes) - len(cityCoordinates)) - 1
                while(size >= 0):
                    current = genome.chromosomes.copy()
                    del current[size]
                    if(fit>prim(current).fitness):
                        del genome.chromosomes[size]
                    size -=1     
        unmutated +=1 
        temp = prim(genome.chromosomes) 
        genome.chromosomes = temp.chromosomes.copy()
        genome.path = temp.path.copy()
        genome.fitness = temp.fitness 

    

def naturalSelection(population,popSize):
    count = 0
    for genome in population:
        population[popSize-1-count] = copy.deepcopy(genome)
        count += 1



def findBestGenome(population):
    allFitness = [i.fitness for i in population]
    bestFitness = min(allFitness)
    return population[allFitness.index(bestFitness)]


def GeneticAlgorithm(popSize, maxgen,points,city):
    global obstacles
    obstacles = points
    global cityCoordinates
    cityCoordinates = city
    start = time.perf_counter()
    global generation
    generation = 0
    global maxGeneration
    maxGeneration = maxgen
    population = CreateNewPopulation(popSize) 
    leadingFitnesses= []
    leadingGenome = Genome()
    bestGenome = Genome()

    while generation < maxGeneration:
        generation += 1
        if(generation > 1):
            population.sort(key=lambda x: x.fitness, reverse=False)
            naturalSelection(population,popSize)
            mutatePopulation(population,maxGeneration-generation,MUTATION_RATE_POINT,MUTATION_RATE_DELETE,MUTATION_RATE_MOVE_POINT)
        leadingGenome = copy.deepcopy(findBestGenome(population)) 
        leadingFitnesses.append(leadingGenome.fitness)
        if(leadingGenome.fitness<bestGenome.fitness):
            bestGenome = copy.deepcopy(leadingGenome)
        # print("Generation: {0}\t\t Max Generation: {1}\nPopulation Size: {2}\t Average Fitness: {3}\nBest Fitness: {4}\n\n\n"
        #     .format(generation, maxGeneration, len(population), average_fitness, bestGenome.fitness))
    gen = Generation()
    gen.timer = int(time.perf_counter()-start)
    gen.leadingFitnesses = leadingFitnesses
    gen.bestGenome = copy.deepcopy(leadingGenome)

    return gen

    