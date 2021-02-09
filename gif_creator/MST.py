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

MUTATION_RATE_DELETE = 15
MUTATION_RATE_POINT = 60
MUTATION_RATE_MOVE_POINT = 100
MUTATION_MOVE_SIZE = 1
FACTOR_INCREASE = 100



cityCoordinates = np.random.uniform(0,100, size=(15,2))





class Genome():
    path = []
    chromosomes = []
    fitness = sys.maxsize


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



def prim(chro):
    MST = Genome()
    MST.chromosomes = chro
    MST.fitness = 0
    path = []
    G = squareform(pdist(chro))
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
        #print(str(x) + "-" + str(y) + ":" + str(G[x][y]))
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
            temp = prim(genome.chromosomes) 
            genome.chromosomes = temp.chromosomes.copy()
            genome.path = temp.path.copy()
            genome.fitness = temp.fitness
        unmutated +=1  

    

def naturalSelection(population,popSize):
    count = 0
    for genome in population:
        population[popSize-1-count] = copy.deepcopy(genome)
        count += 1



def findBestGenome(population):
    allFitness = [i.fitness for i in population]
    bestFitness = min(allFitness)
    return population[allFitness.index(bestFitness)]

def returnGenomes():
    return leaders

def returnMST():
    return prim(cityCoordinates)

leaders= []
def GeneticAlgorithm(popSize, maxGeneration):
    generation = 0
    population = CreateNewPopulation(popSize)
    leadingFitnesses= []
    leadingGenome = Genome()
    bestGenome = Genome()
    global leaders

    while generation < maxGeneration:
        generation += 1
        population.sort(key=lambda x: x.fitness, reverse=False)
        naturalSelection(population,popSize)
        mutatePopulation(population,maxGeneration-generation,MUTATION_RATE_POINT,MUTATION_RATE_DELETE,MUTATION_RATE_MOVE_POINT)
        leadingGenome = copy.deepcopy(findBestGenome(population)) 
        leadingFitnesses.append(leadingGenome.fitness)
        average_fitness = round(np.sum([genom.fitness for genom in population]) / len(population), 2)
        if(leadingGenome.fitness<bestGenome.fitness):
            bestGenome = copy.deepcopy(leadingGenome)
            leaders.append(copy.deepcopy(bestGenome))
        print("Generation: {0}\t\t Max Generation: {1}\nPopulation Size: {2}\t Average Fitness: {3}\nBest Fitness: {4}\n\n\n"
            .format(generation, maxGeneration, len(population), average_fitness, bestGenome.fitness))
    #plot(int(time.perf_counter()-start),generation, leadingFitnesses,bestGenome, startingGenome,obstacles)

    