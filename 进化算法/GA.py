import numpy as np
import matplotlib.pyplot as plt

DNA_SIZE = 10  # DNA length
POP_SIZE = 100  # population size
CROSS_RATE = 0.8  # mating probability (DNA crossover)
MUTATION_RATE = 0.003  # mutation probability
N_GENERATIONS = 200  # the times
X_BOUND = [0, 5]  # x upper and lower bounds


def F(x):
    return np.sin(10 * x) * x + np.cos(2 * x) * x


def get_fitness(pred):
    return pred + 1e-3 - np.min(pred)


def translateDNA(pop):
    return pop.dot(2 ** np.arange(DNA_SIZE)[::-1]) / (2 ** DNA_SIZE - 1) * X_BOUND[1]


def select(pop, fitness):
    idx = np.random.choice(np.arange(POP_SIZE), size=POP_SIZE, replace=True, p=fitness / fitness.sum())
    return pop[idx]


def crossover(parent, pop):
    if np.random.rand() < CROSS_RATE:  # 改进 random产生的数不一定为均匀分布
        i_ = np.random.randint(0, POP_SIZE, size=1)
        cross_points = np.random.randint(0, 2, size=DNA_SIZE).astype(np.bool)
        parent[cross_points] = pop[i_, cross_points]
    return parent


def mutate(child):
    for point in range(DNA_SIZE):
        if np.random.rand() < MUTATION_RATE:
            child[point] = 1 if child[point] == 0 else 0
    return child


pop = np.random.randint(0, 2, (1, DNA_SIZE)).repeat(POP_SIZE, axis=0)  # initialize population

plt.ion()
x = np.linspace(*X_BOUND, 200)
plt.plot(x, F(x))

for _ in range(N_GENERATIONS):
    F_values = F(translateDNA(pop))

    if "sca" in globals():
        sca.remove()
    sca = plt.scatter(translateDNA(pop), F_values, s=200, lw=0, c="red", alpha=0.5)
    plt.pause(0.05)

    fitness = get_fitness(F_values)
    print("Most fitted DNA: ", pop[np.argmax(fitness), :])

    pop = select(pop, fitness)
    pop_copy = pop.copy()

    for parent in pop:
        child = crossover(parent, pop_copy)  # 改进  这里应分为两个部分进行交叉，这样相当于自交没有作用
        child = mutate(child)
        parent[:] = child

plt.ioff()
plt.show()
