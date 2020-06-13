import sys
import time

import matplotlib.pyplot as plt
import numpy as np
import numpy.random as rn

eps = []


def draw_graph(x, y, func):
    """
    Function graphs trace of our swarms
    :param x:
    :param y:
    :param func:
    :return:
    """
    plt.xlabel("X- axis")
    plt.ylabel("Y-yang ")
    plt.title("Particle Swarm")
    for i in range(len(y)):
        plt.plot(x, [func(val) for val in y[i]], label='id %s' % i)
    plt.legend()
    plt.show()


def get_millis(seconds):
    """
    Function returns milliseconds
    :param seconds:
    :return:
    """
    return seconds * 10 ** 3


def get_current_time():
    """
    Function return current time
    :return:
    """
    return get_millis(int(time.time()))


def happy_cat(l):
    """
    Example quality function
    :param l: x vector
    :return:
    """
    x = np.linalg.norm(l)
    x2 = pow(x, 2)
    return 0.5 + pow(pow(x2 - 4, 2), 0.125) + 0.25 * (
            0.5 * x2 + sum(l))


def get_random_x(xi=5, len_x=5):
    """
    Gets random vector x
    :param xi:
    :param len_x:
    :return:
    """
    return [rn.randint(-xi, xi) for _ in range(len_x)]


def get_random_v(vi=1, len_x=5):
    """
    Returns random velocity vector
    :param vi:
    :param len_x:
    :return:
    """
    return [rn.uniform(-vi, vi) for _ in range(len_x)]


def yang(x):
    """
    Yang-Shin function - quality"
    :param x: vector
    :return: yang(x)
    """""
    return sum([eps[i] * pow(np.abs(x[i]), i + 1) for i in range(len(x))])


def get_fittest_informants(previous_exes):
    """
    Find fittest location of all in current generation
    :param previous_exes:
    :return:
    """
    result = False
    for exes in previous_exes:
        if not result or yang(exes[len(exes) - 1]) < yang(result):
            result = exes[len(exes) - 1]
    return result


def get_fittest_personal(i, previous_exes):
    """
    Finds fittest location personally
    :param i:
    :param previous_exes:
    :return:
    """
    result = False
    for exes in previous_exes[i]:
        if not result or yang(exes) < yang(result):
            result = exes
    return result


def get_fittest_all(previous_exes):
    """
    Finds best location til current generation
    :param previous_exes:
    :return:
    """
    result = False
    for i in range(len(previous_exes)):
        for exes in previous_exes[i]:
            if not result or yang(exes) < yang(result):
                result = exes
    return result


def x_range_control(population, epsilon):
    """
    Decides about jumping over, and size of jumpes( and controls range)
    :param population:
    :param epsilon:
    :return:
    """
    for j in range(len(population)):
        for i in range(len(population[j][0])):
            population[j][0][i] += epsilon * population[j][1][i]
            if population[j][0][i] > 5:
                population[j][0][i] = 5 * rn.uniform(-1, 1)
            elif population[j][0][i] < -5:
                population[j][0][i] = -5 * rn.uniform(-1, 1)


def set_best(best, population, func):
    """
    Find best of population (here minimal by func)
    :param best:
    :param population:
    :param func:
    :return:
    """
    for i in range(len(population)):
        x = population[i][0]
        if best is False or func(x) < func(best):
            best = x
    return best


def collect_fittest(i, previous_exes_all):
    """
    :param i:
    :param previous_exes_all:
    :return:  fittest personal, population, any
    """
    return get_fittest_personal(i, previous_exes_all), get_fittest_informants(
        previous_exes_all), get_fittest_all(previous_exes_all)


def particle_swarm(x0, t, func, swarm_size=100, alpha=0.8, beta=0.75, gamma=0.9, delta=0.1, epsilon=1.0, plot=True):
    """
    :param x0: - start vector
    :param t: time limitation
    :param func: quality function
    :param swarm_size: quantity of swarms
    :param alpha: velocity retained
    :param beta: personal best retained
    :param gamma: best of informants' retained
    :param delta: global best retained
    :param epsilon: size of jumps
    :param plot: graphs
    :return:
    """
    end_time = get_current_time() + get_millis(t)
    population = [(x0, get_random_v())]
    best = False

    # Generate swarm_size swarms
    for _ in range(swarm_size):
        new_swarm_x, new_swarm_v = get_random_x(), get_random_v()
        population.append([new_swarm_x, new_swarm_v])
    previous_exes_all = [[el[0]] for el in population]

    while get_current_time() <= end_time:
        # Find best in current population
        best = set_best(best, population, func)

        for i in range(len(population)):
            xi, vi = population[i][0], population[i][1]
            fittest_personal, fittest_informants, fittest_all = collect_fittest(i, previous_exes_all)
            for j in range(len(xi)):
                b, c, d = rn.uniform(0, beta), rn.uniform(0, gamma), rn.uniform(0, delta)
                population[i][1][j] = alpha * vi[j] + b * (fittest_personal[j] - xi[j]) + c * (
                        fittest_informants[j] - xi[j]) + d * (fittest_all[j] - xi[j])

        x_range_control(population, epsilon)

        for i in range(len(population)):
            previous_exes_all[i].append(population[i][0].copy())
    if plot is True:
        draw_graph([i for i in range(len(previous_exes_all[0]))],
                   previous_exes_all, func=yang)
    return best


def modern_particle_swarm(x0, t, func, swarm_size=100, alpha=0.8, beta=0.95, gamma=0.6, delta=0, epsilon=1.0):
    """
    :param x0: - start vector
    :param t: time limitation
    :param func: quality function
    :param swarm_size: quantity of swarms
    :param alpha: velocity retained
    :param beta: personal best retained
    :param gamma: best of informants' retained
    :param delta: global best retained
    :param epsilon: size of jumps
    :return:
    """
    end_time = get_current_time() + get_millis(t)
    population = [(x0, get_random_v())]
    best = False
    # Generate swarm_siz
    for _ in range(swarm_size):
        new_swarm_x, new_swarm_v = get_random_x(), get_random_v()
        population.append([new_swarm_x, new_swarm_v])

    personal_results = [x for x, v in population]

    while get_current_time() <= end_time:
        # Find best in current population
        best = set_best(best, population, func)
        fittest_informants = min(personal_results, key=func)

        for i in range(len(population)):
            xi, vi = population[i][0], population[i][1]
            fittest_personal = personal_results[i]
            fittest_all = best

            for j in range(len(xi)):
                b, c, d = rn.uniform(0, beta), rn.uniform(0, gamma), rn.uniform(0, delta)
                population[i][1][j] = alpha * vi[j] + b * (fittest_personal[j] - xi[j]) + c * (
                        fittest_informants[j] - xi[j]) + d * (fittest_all[j] - xi[j])

        x_range_control(population, epsilon)
        for i in range(len(population)):
            # Personal results update
            if func(population[i][0]) < func(personal_results[i]):
                personal_results[i] = population[i][0]
    return best


def main(args):
    global eps
    t = int(args[0])
    x = [float(x) for x in args[1:6]]
    eps = [float(x) for x in args[6:]]
    best1 = particle_swarm(x, t, func=yang)
    # best1 = modern_particle_swarm(x, t, func=yang)
    print(best1, yang(best1))


main(sys.argv[1:])
