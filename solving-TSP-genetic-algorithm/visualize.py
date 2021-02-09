import matplotlib.pyplot as plt


def plot(generation, allBestFitness, bestGenome, cityLoc, firstGen):
    fig, (ax1,ax2,ax3) = plt.subplots(3)
    fig.suptitle('Simple Genetic TSP Results')
    ax1.set_title("Generations: {0}  Best Fitness: {1}".format(
        generation, bestGenome.fitness), fontsize= 10)
    ax1.plot(range(0, generation), allBestFitness, c="black")

    for x, y in cityLoc:
        ax2.scatter(x, y, c="black")
    xx = [cityLoc[i][0] for i in firstGen.chromosomes]
    yy = [cityLoc[i][1] for i in firstGen.chromosomes]
    for x, y in zip(xx, yy):
        plt.text(x + 2, y - 2, str(yy.index(y)), color="green", fontsize=10)
    ax2.plot(xx, yy, color="red", linewidth=1.75, linestyle="-")
    ax2.set_title("Generation: {0}   Best Fitness: {1}".format(
        0, firstGen.fitness), fontsize= 10)
    

    for x, y in cityLoc:
        ax3.scatter(x, y, c="black")
    xx = [cityLoc[i][0] for i in bestGenome.chromosomes]
    yy = [cityLoc[i][1] for i in bestGenome.chromosomes]
    ax3.plot(xx, yy, color="green", linewidth=1.75, linestyle="-")
    ax3.set_title("Generation: {0}   Best Fitness: {1}".format(
        generation, bestGenome.fitness), fontsize= 10)

    fig.tight_layout()
    plt.show()
