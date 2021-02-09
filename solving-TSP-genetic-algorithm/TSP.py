import numpy as np
import random
import math
from visualize import plot

MUTATION_RATE = 30
MUTATION_REPEAT_COUNT = 3
REPRODUCTION_RATE =  20
POPULATION_GROWTH_RATE = 0
cityCoordinates =  np.random.randint(0,100, size=(15,2))
citySize = len(cityCoordinates)


class Genome():
    chromosomes = []
    fitness = 9999



def CreateNewPopulation(size):
    population = []
    for x in range(size):
        newGenome = Genome()
        newGenome.chromosomes = random.sample(range(1, citySize), citySize - 1)
        newGenome.chromosomes.insert(0, 0)
        newGenome.chromosomes.append(0)
        newGenome.fitness = Evaluate(newGenome.chromosomes)
        population.append(newGenome)
    return population


def distance(a, b):
    dis = math.sqrt(((a[0] - b[0])**2) + ((a[1] - b[1])**2))
    return np.round(dis, 2)


def Evaluate(chromosomes):
    calculatedFitness = 0
    for i in range(len(chromosomes) - 1):
        p1 = cityCoordinates[chromosomes[i]]
        p2 = cityCoordinates[chromosomes[i + 1]]
        calculatedFitness += distance(p1, p2)
    calculatedFitness = np.round(calculatedFitness, 2)
    return calculatedFitness


def findBestGenome(population):
    allFitness = [i.fitness for i in population]
    bestFitness = min(allFitness)
    return population[allFitness.index(bestFitness)]


def TournamentSelection(population, k):
    selected = [population[random.randrange(0, len(population))] for i in range(k)]
    bestGenome = findBestGenome(selected)
    return bestGenome


def Reproduction(population):
    parent1 = TournamentSelection(population, 10).chromosomes
    parent2 = TournamentSelection(population, 10).chromosomes
    while parent1 == parent2:
        parent2 = TournamentSelection(population, 3).chromosomes

    return OrderOneCrossover(parent1, parent2)



def OrderOneCrossover(parent1, parent2):
    size = len(parent1)
    child = [-1] * size

    child[0], child[size - 1] = 0, 0

    point = random.randrange(5, size - 4)

    for i in range(point, point + 4):
        child[i] = parent1[i]
    point += 4
    point2 = point
    while child[point] in [-1, 0]:
        if child[point] != 0:
            if parent2[point2] not in child:
                child[point] = parent2[point2]
                point += 1
                if point == size:
                    point = 0
            else:
                point2 += 1
                if point2 == size:
                    point2 = 0
        else:
            point += 1
            if point == size:
                point = 0

    newGenome = Genome()
    newGenome.chromosomes = child
    newGenome.fitness = Evaluate(child)
    return newGenome


def SwapMutation(chromo):
    for x in range(1,random.randint(1,MUTATION_REPEAT_COUNT+1)):
        p1, p2 = [random.randrange(1, len(chromo) - 1) for i in range(2)]
        while p1 == p2:
            p2 = random.randrange(1, len(chromo) - 1)
        log = chromo[p1]
        chromo[p1] = chromo[p2]
        chromo[p2] = log
    return chromo


def GeneticAlgorithm(popSize, maxGeneration):
    allBestFitness = []
    population = CreateNewPopulation(popSize)
    generation = 0
    netSize = int(len(population))
    firstGen = findBestGenome(population)
    lowestGenome = Genome()
    while generation < maxGeneration:
        generation += 1

        for i in range(netSize):
            if random.randrange(0, 100) < REPRODUCTION_RATE:
                population.append(Reproduction(population))

        for genom in population:
            if random.randrange(0, 100) < MUTATION_RATE:
                genom.chromosomes = SwapMutation(genom.chromosomes)
                genom.fitness = Evaluate(genom.chromosomes)
        
        while(int((len(population))) > popSize+generation*POPULATION_GROWTH_RATE):
            for x in population:
                if x.fitness == max([y.fitness for y in population]):
                    population.remove(x)
                    break
        averageFitness = round(np.sum([genom.fitness for genom in population]) / len(population), 2)
        bestGenome = findBestGenome(population)
        if(lowestGenome.fitness>bestGenome.fitness):
            lowestGenome = bestGenome
        print("\n" * 5)
        print("Generation: {0}\t\t Max Generation: {1}\nPopulation Size: {2}\t Average Fitness: {3}\nBest Fitness: {4}"
              .format(generation, maxGeneration, len(population), averageFitness,
                      lowestGenome.fitness))
        allBestFitness.append(bestGenome.fitness)

    plot(generation, allBestFitness, lowestGenome, cityCoordinates,firstGen)


if __name__ == "__main__":
    GeneticAlgorithm(popSize=100, maxGeneration=50)
