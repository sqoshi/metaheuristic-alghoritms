import sys
import time

import matplotlib.pyplot as plt
import numpy as np
import numpy.random as rn

eps = []


def draw_graph(x, y, func):
    plt.xlabel("X- axis")
    plt.ylabel("Y-yang ")
    plt.title("Particle Swarm")
    for i in range(len(y)):
        plt.plot(x, [func(val) for val in y[i]], label='id %s' % i)
    plt.legend()
    plt.show()


def get_millis(seconds):
    return seconds * 10 ** 3


def get_current_time():
    return get_millis(int(time.time()))


def happy_cat(l):
    x = np.linalg.norm(l)
    x2 = pow(x, 2)
    return 0.5 + pow(pow(x2 - 4, 2), 0.125) + 0.25 * (
            0.5 * x2 + sum(l))


def get_random_x():
    return [rn.randint(-2, 2) for _ in range(5)]


def get_random_v():
    return [rn.uniform(-1, 1) for _ in range(5)]


def yang(x):
    return sum([eps[i] * pow(np.abs(x[i]), i + 1) for i in range(len(x))])


def get_previous_informators_fittest(previous_exes):
    result = False
    for exes in previous_exes:
        if not result or yang(exes[len(exes) - 1]) < yang(result):
            result = exes[len(exes) - 1]
    return result


def get_previous_fittest(i, previous_exes):
    result = False
    for exes in previous_exes[i]:
        if not result or yang(exes) < yang(result):
            result = exes
    return result


def get_previous_fittest_all(previous_exes):
    result = False
    for i in range(len(previous_exes)):
        for exes in previous_exes[i]:
            if not result or yang(exes) < yang(result):
                result = exes
    return result


def x_range_control(population, epsilon):
    for j in range(len(population)):
        for i in range(len(population[j][0])):
            population[j][0][i] += epsilon * population[j][1][i]
            if population[j][0][i] > 5:
                population[j][0][i] = 5
            if population[j][0][i] < -5:
                population[j][0][i] = -5


def collect_fittest(i, previous_exes_all):
    return get_previous_fittest(i, previous_exes_all), get_previous_informators_fittest(
        previous_exes_all), get_previous_fittest_all(previous_exes_all)


def particle_swarm(x0, t, func, swarm_size=4, alpha=0.8, beta=0.75, gamma=0.9, delta=0.1, epsilon=1.0):
    end_time = get_current_time() + get_millis(t)
    population = [(x0, get_random_v())]
    best = False

    for _ in range(swarm_size):
        new_swarm_x, new_swarm_v = get_random_x(), get_random_v()
        population.append([new_swarm_x, new_swarm_v])
    previous_exes_all = [[el[0]] for el in population]

    while get_current_time() <= end_time:

        for i in range(len(population)):
            x, v = population[i][0], population[i][1]

            if best is False or func(x) < func(best):
                best = x

        for i in range(len(population)):
            xi, vi = population[i][0], population[i][1]
            x_prev_fittest, x_prev_info_fittest, x_prev_fittest_all = collect_fittest(i, previous_exes_all)
            for j in range(len(xi)):
                b, c, d = rn.uniform(0, beta), rn.uniform(0, gamma), rn.uniform(0, delta)
                population[i][1][j] = alpha * vi[j] + b * (x_prev_fittest[j] - xi[j]) + c * (
                        x_prev_info_fittest[j] - xi[j]) + d * (x_prev_fittest_all[j] - xi[j])

        x_range_control(population, epsilon)
        for i in range(len(population)):
            # print('x', population[i][0], func(population[i][0]))
            previous_exes_all[i].append(population[i][0].copy())
        # print()
    for ex in np.array(previous_exes_all).T:
        print(ex)
    draw_graph([i for i in range(len(previous_exes_all[0]))], previous_exes_all, func=yang)
    return best


def main(args):
    global eps
    t = int(args[0])
    x = [float(x) for x in args[1:6]]
    eps = [float(x) for x in args[6:]]
    print('t=', t)
    print('x=', x)
    print('E=', eps)
    best = particle_swarm(x, t, func=yang)
    print(best, yang(best))


main(sys.argv[1:])
