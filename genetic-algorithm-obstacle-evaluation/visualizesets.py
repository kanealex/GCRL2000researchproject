import matplotlib.pyplot as plt
from math import log10, floor
import MSTclassic
import numpy as np

def plotgens(classic,algorithm1,adaptive, algorithm2,startingGenome, generation, obstacle,trials):
    fig, (ax1,ax2,ax3) = plt.subplots(3)
    ax2.autoscale(False)
    ax3.autoscale(False)
    ax2.set(xlim=(0,110), ylim=(0,110))
    ax3.set(xlim=(0,110), ylim=(0,110))

    alg1improvement = ((startingGenome.fitness - algorithm1.bestGenome.fitness)/startingGenome.fitness)*100
    if(alg1improvement<=0):
        alg1improvement=0.00000000001
    alg2improvement = ((startingGenome.fitness - algorithm2.bestGenome.fitness)/startingGenome.fitness)*100
    if(alg2improvement<=0):
        alg2improvement=0.00000000001
    

    classic1 = []
    for x in classic:
        classic1.append(((startingGenome.fitness-x)/startingGenome.fitness)*100)

    adaptive1 = []
    for x in adaptive:
        adaptive1.append(((startingGenome.fitness-x)/startingGenome.fitness)*100)


    if(np.average(classic1) > np.average(adaptive1)):
        x = round_sig(((np.average(classic1)-np.average(adaptive1))/np.average(classic1))*100,4)
        fig.suptitle('Classic Algorithm {0}% Improvement on Adaptive'.format(x))
    else:
        x = round_sig(((np.average(adaptive1)-np.average(classic1))/np.average(adaptive1))*100,4)
        fig.suptitle('Adpative Algorithm {0}% Improvement on Classic'.format(x))
    
    
    ax1.set_title( "Classic (GREEN) Average: {0}%     Adaptive (RED) Average: {1}%".format(round_sig(np.average(classic1),6),round_sig(np.average(adaptive1),6)) , fontsize= 10)


    ax1.plot(range(0, trials), classic, c="green")
    ax1.plot(range(0, trials), adaptive, c="red")


    for x, y in algorithm1.bestGenome.chromosomes:
        ax2.scatter(x,y,c="blue")
    for x, y in algorithm2.bestGenome.chromosomes:
        ax3.scatter(x,y,c="blue")
    
    for x, y in startingGenome.chromosomes:
        ax2.scatter(x, y, c="black")
        ax3.scatter(x,y,c="black")
 
    for a in algorithm1.bestGenome.path:
        x1 = algorithm1.bestGenome.chromosomes[a[0]][0]
        y1 = algorithm1.bestGenome.chromosomes[a[0]][1] 
        x2 = algorithm1.bestGenome.chromosomes[a[1]][0]
        y2 = algorithm1.bestGenome.chromosomes[a[1]][1]
        if(MSTclassic.collide([x1,y1],[x2,y2])):
             ax2.plot([x1,x2],[y1,y2],'k-',color='orange')
        else:
            ax2.plot([x1,x2],[y1,y2],'k-')
    ax2.set_title("Best Classic MST: {0}   End Fitness: {1}".format(round_sig(alg1improvement,6), round_sig(algorithm1.bestGenome.fitness,4)), fontsize= 10)

    for a in algorithm2.bestGenome.path:
        x1 = algorithm2.bestGenome.chromosomes[a[0]][0]
        y1 = algorithm2.bestGenome.chromosomes[a[0]][1] 
        x2 = algorithm2.bestGenome.chromosomes[a[1]][0]
        y2 = algorithm2.bestGenome.chromosomes[a[1]][1] 
        if(MSTclassic.collide([x1,y1],[x2,y2])):
             ax3.plot([x1,x2],[y1,y2],'k-',color='orange')
        else:
            ax3.plot([x1,x2],[y1,y2],'k-')
    ax3.set_title("Best Adaptive MST: {0}   End Fitness: {1}".format(round_sig(alg2improvement,6), round_sig(algorithm2.bestGenome.fitness,4)), fontsize= 10)
    

    if(len(obstacle)>0):
        obstacle.append(obstacle[0]) #repeat the first point to create a 'closed loop'
        xs, ys = zip(*obstacle) #create lists of x and y values
        ax3.plot(xs,ys, color = 'grey')
        ax2.plot(xs,ys, color = 'grey')


    fig.tight_layout()
    plt.show()

def round_sig(x, sig=2):
    return round(x, sig-int(floor(log10(abs(x))))-1)