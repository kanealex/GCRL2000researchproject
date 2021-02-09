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

a = [[1,0],[2,0],[3,0],[4,0],[5,0]]


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

    for x in range(len(chromosomes)):    
        calc = hypot(chromosomes[x][0]-chromosomes[pointpos][0], chromosomes[x][1]-chromosomes[pointpos][1])
        oldarray[x][pointpos] = calc
        oldarray[pointpos][x] = calc
    return oldarray
 
def deletesquarearray(oldarray,pointpos):
    del oldarray[pointpos]
    for x in range(len(oldarray)):
        oldarray[x].pop(pointpos)
    return oldarray




b = squareform(createdistances(a))
c = b.tolist()
h = [[1,0],[2,0],[4,0],[5,0]]

c = deletesquarearray(c,2)

print("REAL")
print(squareform(createdistances(h)))
print("FAKE")
print(c)
