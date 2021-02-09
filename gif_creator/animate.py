#animate the genetic algorithm learning by graphing the best genome generation by generation
#no obstacle implementation (can add obstacles in the animateMST)

import matplotlib.pyplot as plt
import matplotlib.animation as animation
import MST

NUMBER_OF_GENERATIONS = 500
NUMBER_OF_GENOMES = 20







intervalnumber = 0
MST.GeneticAlgorithm(NUMBER_OF_GENOMES,NUMBER_OF_GENERATIONS)
points = MST.getPoints()
mst = MST.returnMST()
listofgenomes = MST.returnGenomes()
fig = plt.figure()
ax1 = fig.add_subplot(1,1,1)
ax1.autoscale(False)
ax1.set(xlim=(0,110), ylim=(0,110))

def animate(i):
    ax1.clear()
    global intervalnumber
    if(intervalnumber<10):
        for x, y in points:
            ax1.scatter(x,y,c="black")
    elif(intervalnumber<15):
        for x, y in points:
            ax1.scatter(x,y,c="black")
        for b in mst.path:
            x1 = mst.chromosomes[b[0]][0]
            y1 = mst.chromosomes[b[0]][1] 
            x2 = mst.chromosomes[b[1]][0]
            y2 = mst.chromosomes[b[1]][1] 
            ax1.plot([x1,x2],[y1,y2],'k-')
    elif(len(listofgenomes)> 0):
        a = listofgenomes[0]
        if(len(listofgenomes)!=1):
            del listofgenomes[0]
        for x, y in a.chromosomes:
            ax1.scatter(x,y,c="blue")
        for x, y in points:
            ax1.scatter(x, y, c="black")
        for b in a.path:
            x1 = a.chromosomes[b[0]][0]
            y1 = a.chromosomes[b[0]][1] 
            x2 = a.chromosomes[b[1]][0]
            y2 = a.chromosomes[b[1]][1] 
            ax1.plot([x1,x2],[y1,y2],'k-')

    plt.title('Genetic Power Grid Algorithm')	
    intervalnumber+=1
    
ani = animation.FuncAnimation(fig, animate, interval=100, frames=100) 


plt.show()
