import random
import sys
import time
from math import sqrt, cos

import numpy as np


def sum_of_quadrates(l):
    s = 0
    for x in l:
        s += pow(x, 2)
    return s


def products_of_cos(l):
    p = 1
    for i in range(len(l)):
        p *= cos(l[i] / sqrt(i + 1))
    return p


def griewank(l):
    s = sum_of_quadrates(l)
    p = products_of_cos(l)
    return 1 + 1 / 4000 * s - p


def happy_cat(l):
    x = np.linalg.norm(l)
    x2 = pow(x, 2)
    return 0.5 + pow(pow(x2 - 4, 2), 0.125) + 0.25 * (
            0.5 * x2 + sum(l))


def get_neighbour(x):
    return [xi + random.uniform(-1, 1) for xi in x]


def get_func(b):
    if b == 0:
        return happy_cat
    else:
        return griewank


def get_environment(x):
    return [get_neighbour(x) for _ in range(100)]


def get_time():
    return int(round(time.time() * 1000))


def hill_climbing(t, quality):
    T = t * 1000
    end_time = get_time() + T
    S = [random.uniform(-5, 5) for _ in range(4)]
    best = S
    while get_time() < end_time:
        time_local = random.randint(get_time(), end_time)
        while get_time() < time_local:
            R = get_neighbour(S)
            if quality(R) < quality(S):
                S = R
        if quality(S) < quality(best):
            best = S
        S = [random.uniform(-5, 5) for _ in range(4)]
    return best


def local_search(t, quality):
    end_time = get_time() + t * 1000
    x = [random.uniform(-5, 5) for _ in range(4)]
    best_solution = x
    while get_time() < end_time:
        x = min(get_environment(x), key=quality)
        if x == best_solution:
            x = [random.uniform(-5, 5) for _ in range(4)]
        if quality(x) < quality(best_solution):
            best_solution = x
    return best_solution


def main():
    line = input()
    s = line.split()
    if len(s) < 2:
        sys.stderr.write('You need to input 2 args')
        sys.exit(0)
    try:
        t, b = int(s[0]), int(s[1])
    except ValueError:
        sys.stderr.write('Could not parse values')
        sys.exit(0)
    result = local_search(t, get_func(b))
    r1 = hill_climbing(t, get_func(b))
    print(result, get_func(b)(result))
    print(r1, get_func(b)(r1))


main()
