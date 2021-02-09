import matplotlib.pyplot as plt
from math import log10, floor


def plot(time, generation, allBestFitness, finalPath, firstPath):
    fig, (ax1,ax2,ax3) = plt.subplots(3)
    a = ((firstPath.fitness - finalPath.fitness)/firstPath.fitness)*100
    fig.suptitle('Genetic MSP Results'.format(time))
    ax1.set_title("Calculation Time: {0} seconds  Improvement: {1}%".format(
        time,round_sig(a,4)), fontsize= 10)
    ax1.plot(range(0, generation), allBestFitness, c="green")

    for x, y in finalPath.chromosomes:
            ax3.scatter(x,y,c="blue")

    for x, y in firstPath.chromosomes:
        ax2.scatter(x, y, c="black")
        ax3.scatter(x,y,c="black")

    for a in firstPath.path:
        x1 = firstPath.chromosomes[a[0]][0]
        y1 = firstPath.chromosomes[a[0]][1] 
        x2 = firstPath.chromosomes[a[1]][0]
        y2 = firstPath.chromosomes[a[1]][1]  
        ax2.plot([x1,x2],[y1,y2],'k-')
    ax2.set_title("Generation: {0}   Start Fitness: {1}".format(
        0, round_sig(firstPath.fitness,5)), fontsize= 10)

    for a in finalPath.path:
        x1 = finalPath.chromosomes[a[0]][0]
        y1 = finalPath.chromosomes[a[0]][1] 
        x2 = finalPath.chromosomes[a[1]][0]
        y2 = finalPath.chromosomes[a[1]][1]  
        ax3.plot([x1,x2],[y1,y2],'k-')
    ax3.set_title("Generation: {0}   Best Fitness: {1}".format(
        generation, round_sig(finalPath.fitness,5)), fontsize= 10)
    

    fig.tight_layout()
    plt.show()

def round_sig(x, sig=2):
    return round(x, sig-int(floor(log10(abs(x))))-1)