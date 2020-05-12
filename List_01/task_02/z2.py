import itertools
import random
import time


def read_data(filename):
    f = open(filename, "r")
    line = f.readline()
    t, n = line.split()
    line = f.readline()
    array = []
    while line:
        array.append([int(x) for x in line.split()])
        line = f.readline()
    return t, n, array


def get_new_city(n, src):
    city = random.randint(1, n - 1)
    while src == city:
        city = random.randint(1, n - 1)
    return city


def get_distance(graph, path):
    distance = 0
    for i in range(0, len(path) - 1):
        distance += graph[path[i]][path[i + 1]]
    return distance


def swap_positions(list, pos1, pos2):
    l = list.copy()
    l[pos1], l[pos2] = l[pos2], l[pos1]
    return l


def get_all_swaps(list):
    result = []
    for i, j in itertools.combinations([i for i in range(len(list))], 2):
        result.append(swap_positions(list, i, j))
    return result


def get_swapped(list):
    i = random.randint(0, len(list) - 1)
    j = random.randint(0, len(list) - 1)
    while j == i:
        j = random.randint(0, len(list) - 1)
    return swap_positions(list, i, j)


def get_next_city(graph, T):
    city = T[0]
    initialMinium = 0
    row = graph[T[len(T) - 1]]
    for i in range(len(row)):
        if i not in T:
            if initialMinium > row[i] or initialMinium == 0:
                initialMinium = row[i]
                city = i
    return city


def get_initial(graph, n, src):
    T = [src]
    for i in range(n):
        minimalCity = get_next_city(graph, T)
        T.append(minimalCity)
    return T


def set_cycles(list, src):
    for element in list:
        element.insert(0, src)
        element.append(src)
    return list


def set_cycle(element, src):
    element.insert(0, src)
    element.append(src)
    return element


def tabu_search(t, graph, n, src, teleportation, resets, scale=1.5, l=100, tweaks_no=2):
    end_time = int(round(time.time() * 1000)) + t * 1000
    initial = get_initial(graph, n, src)
    best_path, best_dist = initial, get_distance(graph, initial)
    x = initial
    Tabu = [initial]
    while int(round(time.time() * 1000)) < end_time:
        if len(Tabu) > l:
            Tabu.pop(0)
        R = set_cycle(get_swapped(x[1:len(x) - 1]), src)
        for _ in range(tweaks_no - 1):
            W = set_cycle(get_swapped(x[1:len(x) - 1]), src)
            if W not in Tabu and (get_distance(graph, W) < get_distance(graph, R) or R in Tabu):
                R = W
        if R not in Tabu:
            x = R
            Tabu.append(R)
        if get_distance(graph, x) < get_distance(graph, best_path):
            best_path = x
        if resets and get_distance(graph, x) > scale * get_distance(graph, best_path):
            x = best_path
            if teleportation:
                city = get_new_city(n, src)
                src = city
                x = get_initial(graph, n, city)
    return best_path


def modern_tabu_search(t, graph, n, src):
    end_time = int(round(time.time() * 1000)) + t * 1000
    initial = get_initial(graph, n, src)
    best_path, best_dist = initial, get_distance(graph, initial)
    x = initial
    T = []
    while int(round(time.time() * 1000)) < end_time:
        neighbours = set_cycles(get_all_swaps(x[1:len(x) - 1]), src)
        mins = get_distance(graph, neighbours[0])
        for neigh in neighbours:
            if neigh not in T:
                sample = get_distance(graph, neigh)
                if sample <= mins:
                    mins = sample
                    x = neigh
                    if best_dist >= sample:
                        best_dist = sample
                        best_path = x
                    T.append(neigh)
    return best_path


def main():
    # t, n = [int(x) for x in input().split()]
    # g = [[int(x) for x in input().split()] for i in range(n)]
    t, n, g = read_data('tests/data1')
    result = tabu_search(int(t), g, int(n), src=26, resets=True, teleportation=False)
    print(result, get_distance(g, result))


main()
