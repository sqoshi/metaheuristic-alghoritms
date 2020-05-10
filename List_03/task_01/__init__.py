import sys
import time

import numpy as np
import numpy.random as rn


def get_random_x():
    return [rn.randint(-4, 4) for _ in range(5)]


eps = []


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


def particle_swarm(x0, t):
    startTime = int(round(time.time() * 1000))
    endTime = startTime + t * 1000
    swarm_size = 2
    alpha = 0.75
    beta = 0.75
    gamma = 0.75
    delta = 0.25
    epsilon = 1.0
    P = [(x0, get_random_v())]
    best = False
    for _ in range(swarm_size):
        new_swarm_x, new_swarm_v = get_random_x(), get_random_v()
        P.append([new_swarm_x, new_swarm_v])
    previous_exes_all = [[el[0]] for el in P]
    while int(round(time.time() * 1000)) <= endTime:
        for i in range(len(P)):
            x, v = P[i][0], P[i][1]
            if best is False or yang(x) < yang(best):
                best = x
                print(best)
        for i in range(len(P)):
            xi, vi = P[i][0], P[i][1]
            x_prev_fittest = get_previous_fittest(i, previous_exes_all)
            x_prev_info_fittest = get_previous_informators_fittest(previous_exes_all)
            x_prev_fittest_all = get_previous_fittest_all(previous_exes_all)
            for j in range(len(xi)):
                b, c, d = rn.uniform(0, beta), rn.uniform(0, gamma), rn.uniform(0, delta)
                P[i][1][j] = alpha * vi[j] + b * (x_prev_fittest[j] - xi[j]) \
                             + c * (x_prev_info_fittest[j] - xi[j]) \
                             + d * (x_prev_fittest_all[j] - xi[j])
        for x, v in P:
            for i in range(len(x)):
                x[i] += epsilon * v[i]
        for i in range(len(P)):
            previous_exes_all[i].append(P[i][0])

    return best


def main(args):
    global eps
    t = int(args[0])
    x = [float(x) for x in args[1:6]]
    eps = [float(x) for x in args[6:]]
    print('t=', t)
    print('x=', x)
    print('E=', eps)
    best = particle_swarm(x, t)
    print(best, yang(best))


main(sys.argv[1:])
