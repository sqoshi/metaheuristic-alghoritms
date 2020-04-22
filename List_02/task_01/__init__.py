import math
import random
import time

import matplotlib.pyplot as plt
import numpy as np
import numpy.random as rn


def plot_graphs(states, costs):
    """Function to draw states and costs graph."""
    plt.figure()
    plt.subplot(121)
    plt.plot(states, 'r')
    plt.title("States")
    plt.subplot(122)
    plt.plot(costs[10:], 'b')
    plt.title("Costs")
    plt.show()


def salomon(x):
    """Salomon's Function"""
    sum_of_squares = math.sqrt(sum([pow(xi, 2) for xi in x]))
    return 1 - (math.cos(2 * math.pi * sum_of_squares)) + 0.1 * sum_of_squares


def random_neighbour(x, step):
    """Random neighbour generating function"""
    if step % 2 == 0:
        return [xi * (1 + (random.uniform(-1, 1))) for xi in x]
    else:
        return [xi + random.uniform(-4, 4) for xi in x]


def acceptance_probability(cost, new_cost, temp):
    if new_cost < cost:
        return 1
    else:
        p = np.exp(- (new_cost - cost) / temp)
        return p


def simulated_annealing(t, start, T0, resets, graphs):
    """Function simulating annealing"""
    # Find end time
    startTime = int(round(time.time() * 1000))
    endTime = startTime + t * 1000
    T = T0
    # set initial solution
    state = start
    cost = salomon(state)
    states, costs = [state], [cost]
    step = 1
    # while we have time and temperature is bigger than 0.
    while int(round(time.time() * 1000)) <= endTime and T > 0:
        step += 1
        # Decrease temperature
        T *= 0.99
        # If user prefers to use resets, it's implemented.
        if resets and cost > costs[len(costs) - 1] and step % 500000 == 0:
            state, cost = states[len(states) - 1], costs[len(costs) - 1]
        # Generate neighbour
        new_state = random_neighbour(state, step)
        new_cost = salomon(new_state)
        # if probability is bigger than float from range 0,1 ( The less time  we have the less we jump to worse x)
        if acceptance_probability(cost, new_cost, T) > rn.random():
            state, cost = new_state, new_cost
            # Let's make history of our bests for example to make beautiful diagram cost/n.
            if costs[len(costs) - 1] > cost:
                states.append(state)
                costs.append(cost)
    if graphs:
        plot_graphs(states, costs)
    return states, costs


def main(args):
    duration = int(args.split()[0])  # in seconds
    x = [int(i) for i in args.split()[1:]]

    states, costs = simulated_annealing(duration, x, T0=10000, resets=False, graphs=True)

    for x in states[len(states) - 1]:
        print(x, end=' ')
    print(costs[len(costs) - 1])


main(input())
