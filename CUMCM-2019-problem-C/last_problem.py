import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

POP_SIZE = 100  # population size
CROSS_RATE = 0.6  # mating probability (DNA crossover)
MUTATION_RATE = 0.01  # mutation probability
N_GENERATIONS = 300  # the times

#
DNA_SIZE = 2
ASCII_BOUND = [20, 40, 20, 100]


class GA:
    def __init__(self, DNA_size, DNA_bound, cross_rate, mutate_rate, pop_size):
        self.DNA_size = DNA_size
        DNA_bound[1] += 1
        DNA_bound[3] += 1
        self.DNA_bound = DNA_bound
        self.cross_rate = cross_rate
        self.mutate_rate = mutate_rate
        self.pop_size = pop_size
        self.data = pd.read_excel("last_result.xlsx")
        self.data = self.data[self.data["Passenger_State"] == 1]
        # self.pop = np.random.randint(*DNA_bound, size=(pop_size, DNA_size)).astype(np.int8)
        self.pop = np.hstack((np.random.randint(self.DNA_bound[0], self.DNA_bound[1], size=(self.pop_size, 1)),
                              np.random.randint(self.DNA_bound[2], self.DNA_bound[3], size=(self.pop_size, 1))))

    def get_fitness(self):
        match_count = np.zeros((self.pop_size, 1))
        cnt = 0
        for one in self.pop:
            x = one[0]
            n = one[1]
            h_data = self.data[(self.data["Total_Path"] / 1000 > x) & (self.data["Total_Path"] != 0)].iloc[
                     np.random.randint(
                         len(self.data[(self.data["Total_Path"] / 1000 > x) & (self.data["Total_Path"] != 0)])), :]
            l_data = self.data[(self.data["Total_Path"] / 1000 <= x) & (self.data["Total_Path"] != 0)].iloc[
                     np.random.randint(
                         len(self.data[(self.data["Total_Path"] / 1000 <= x) & (self.data["Total_Path"] != 0)])), :]
            l_C1 = 0
            h_C1 = 0
            if l_data["Total_Path"] / 1000 <= 3:
                l_C1 = 11
            elif l_data["Total_Path"] / 1000 > 3:
                l_C1 = 11 + (int(l_data["Total_Path"] / 1000) + 1) * 2.1
            l_C1 += n
            if h_data["Total_Path"] / 1000 <= 3:
                h_C1 = 11
            elif h_data["Total_Path"] / 1000 > 3:
                h_C1 = 11 + (int(l_data["Total_Path"] / 1000) + 1) * 2.1
            match_count[cnt][0] = (l_C1 + h_C1) / (2 * l_C1 * h_C1) + (np.abs(h_C1 - l_C1))
            cnt += 1
        return match_count

    def select(self):
        fitness = self.get_fitness() + 1e-4
        fitness = fitness.ravel()
        idx = np.random.choice(np.arange(self.pop_size), size=self.pop_size, replace=True, p=fitness / fitness.sum())
        return self.pop[idx]

    def crossover(self, parent, pop):
        if np.random.rand() < self.cross_rate:
            i_ = np.random.randint(0, self.pop_size, size=1)
            cross_points = np.random.randint(0, 2, self.DNA_size).astype(np.bool)
            parent[cross_points] = pop[i_, cross_points]
        return parent

    def mutate(self, child):
        for point in range(self.DNA_size):
            if np.random.rand() < self.mutate_rate:
                child[point] = np.random.randint(self.DNA_bound[2 * point], self.DNA_bound[2 * point + 1])
        return child

    def evolve(self):
        pop = self.select()
        pop_copy = pop.copy()
        for parent in pop:
            child = self.crossover(parent, pop_copy)
            child = self.mutate(child)
            parent[:] = child
        self.pop = pop


if __name__ == '__main__':
    ga = GA(DNA_size=DNA_SIZE, DNA_bound=ASCII_BOUND, cross_rate=CROSS_RATE, mutate_rate=MUTATION_RATE,
            pop_size=POP_SIZE)
    nn = []
    kk = []
    data = pd.read_excel("last_result.xlsx")
    data = data[data["Passenger_State"] == 1]

    for generation in range(N_GENERATIONS):
        fitness = ga.get_fitness()
        best_DNA = ga.pop[np.argmin(fitness)]
        print("Gen", generation, ": ", best_DNA)
        x = best_DNA[0]
        n = best_DNA[1]
        h_data = data[(data["Total_Path"] / 1000 > x) & (data["Total_Path"] != 0)].iloc[
                 np.random.randint(
                     len(data[(data["Total_Path"] / 1000 > x) & (data["Total_Path"] != 0)])), :]
        l_data = data[(data["Total_Path"] / 1000 <= x) & (data["Total_Path"] != 0)].iloc[
                 np.random.randint(
                     len(data[(data["Total_Path"] / 1000 <= x) & (data["Total_Path"] != 0)])), :]
        l_C1 = 0
        h_C1 = 0
        if l_data["Total_Path"] / 1000 <= 3:
            l_C1 = 11
        elif l_data["Total_Path"] / 1000 > 3:
            l_C1 = 11 + (int(l_data["Total_Path"] / 1000) + 1) * 2.1
        l_C1 += n
        if h_data["Total_Path"] / 1000 <= 3:
            h_C1 = 11
        elif h_data["Total_Path"] / 1000 > 3:
            h_C1 = 11 + (int(l_data["Total_Path"] / 1000) + 1) * 2.1
        print(l_C1, h_C1)
        print((np.abs(h_C1 - l_C1)))
        nn.append(best_DNA[0])
        kk.append(best_DNA[1])
        ga.evolve()
    plt.plot(np.arange(len(nn)), nn)
    plt.plot(np.arange(len(kk)), kk)
    plt.show()
