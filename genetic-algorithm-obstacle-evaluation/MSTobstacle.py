#compares the adaptive obstacle function with the classic function
#left click to add obstacle points 
#right click to complete


import tkinter as tk
import MSTclassic
import MSTadaptive
import time
import numpy as np
from visualize import plot
from visualizesets import plotgens
import copy

popsize = 30
gen = 50
trials = 100
obstacle = []
draw = []


def myfunction(event):
    x, y = event.x, event.y
    draw.append([x,y])
    obstacle.append([x/10,(1000-y)/10])
    canvas.create_oval(x-2, y-2, x+2,y+2, fill="grey", outline="grey", width=1)
    if canvas.old_coords:
        x1, y1 = canvas.old_coords
        canvas.create_line(x, y, x1, y1,fill="grey",width = 3)
    canvas.old_coords = x, y

def polygon(event):
    if(len(obstacle)>1):
        canvas.create_line(draw[0][0], draw[0][1], draw[len(draw)-1][0], draw[len(draw)-1][1],fill="grey",width = 3)
    root.after(500,exit)
    
def exit():
    root.destroy()
    bestclassic = MSTclassic.Generation()
    classic = []
    bestadaptive = MSTadaptive.Generation()
    adaptive = []

    for x in range(0,trials):
        a = MSTclassic.GeneticAlgorithm(popsize,gen,obstacle,points)
        b = MSTadaptive.GeneticAlgorithm(popsize,gen,obstacle,points)
        # uncomment if want to compare a single runs
        # initial = MSTclassic.prim(points)
        # plot(a,b,initial,gen,obstacle)
        classic.append(a.bestGenome.fitness)
        adaptive.append(b.bestGenome.fitness)
        if(bestclassic.bestGenome.fitness > a.bestGenome.fitness):
            bestclassic = copy.copy(a)
        if(bestadaptive.bestGenome.fitness > b.bestGenome.fitness):
            bestadaptive = copy.copy(b)
    initial = MSTclassic.prim(points)
    plotgens(classic,bestclassic,adaptive,bestadaptive,initial, gen,obstacle,trials)

root = tk.Tk()
canvas = tk.Canvas(root, width=1000, height=1000)
canvas.pack()
canvas.old_coords = None
points = np.random.uniform(0,100, size=(5,2))
for x,y in points:
    canvas.create_oval((10*x)-5, 1000-(10*y)-5, (10*x)+5,1000-(10*y)+5, fill="blue", outline="blue", width=1)

root.bind('<Button-1>', myfunction)
root.bind('<Button-3>', polygon)


root.mainloop()