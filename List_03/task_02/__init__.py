import copy
import random
import time

import numpy as np


####################################################################################
############################## Data Reading ########################################
####################################################################################

def read_data(filepath):
    c, p = [], []
    words = []
    f = open(filepath, "r")
    line = f.readline()
    t, n, s = [int(item) for item in line.split() if item != '\n']
    for i in range(n):
        ci, pi = f.readline().split()
        c += [ci]
        p += [int(pi)]
    for i in range(s):
        words += [f.readline().split()[0]]
    f.close()
    return t, n, s, c, p, words


####################################################################################
########################### Time Operations ########################################
####################################################################################
def get_millis(seconds):
    return seconds * 10 ** 3


def get_current_time():
    return get_millis(int(time.time()))


####################################################################################
########################## Building section ########################################
####################################################################################

def build_letter_dictionary(letters, weights):
    dictionary = {}
    for i in range(len(letters)):
        dictionary[letters[i]] = weights[i]
    return dictionary


def build_frequency_dictionary(letters):
    return {i: int(letters.count(i)) for i in set(letters)}


####################################################################################
################################ Quality ###########################################
####################################################################################
def quality(word, dictionary):
    """Quality Function"""
    summary = 0
    for char in word:
        try:
            summary += dictionary[char]
        except KeyError:
            raise ValueError('Quality function tried to compare word with symbol outside the dictionary')
    return summary


def get_maximal_in(Population, dictionary):
    qualities = []
    for word in Population:
        qualities += [quality(word, dictionary)]
    return Population[qualities.index(max(qualities))]


####################################################################################
########################### Control Section ########################################
####################################################################################
def is_in_dict(word):
    """Function check if word is in dictionary."""
    with open('dict') as f:
        if word in f.read():
            return True
    return False


def are_frequencies_right(word, frequencies):
    """Function validates quantity of each symbol in word as in frequencies."""
    word_dict = build_frequency_dictionary(list(word))
    for key in word_dict:
        try:
            quantity_char = frequencies.get(key)
            if quantity_char is None:
                raise KeyError
            if quantity_char < word_dict.get(key):
                return False
        except KeyError:
            return False
    return True


def is_word_accepted(word, frequencies):
    """Check all conditions."""
    if are_frequencies_right(word, frequencies) and is_in_dict(word):
        return True
    return False


def select_parents(P, dictionary):
    """Selects parents with probability (quality(x_i)/sum(quality(X))"""
    total_sum = sum([quality(pi, dictionary) for pi in P])
    qualities = [quality(pi, dictionary) / total_sum for pi in P]
    result = [False for _ in range(len(P))]
    while result.count(True) < 2:
        for i in range(len(result)):
            if result.count(True) == 2:
                break
            if np.random.uniform(0, 1) < qualities[i]:
                result[i] = True
    g = (i for i, e in enumerate(result) if e == True)
    i = next(g)
    j = next(g)
    return P[i], P[j]


def cross_over(path1, path2):
    """Mixing our genotypes."""
    l1, l2 = len(path1), len(path2)
    c1, d1 = np.random.randint(0, l1 - 1), np.random.randint(0, l1 - 1)
    c2, d2 = np.random.randint(0, l2 - 1), np.random.randint(0, l2 - 1)
    if c1 > d1:
        c1, d1 = d1, c1
    if c2 > d2:
        c2, d2 = d2, c2
    return path1[:c1] + path2[c2:d2] + path1[d1:], path2[:c2] + path1[c1:d1] + path1[d2:]


def two_point_crossover(path1, path2, frequencies):
    """Controls that our new paths are correct."""
    new_path1, new_path2 = cross_over(path1, path2)
    counter = 0
    while not is_word_accepted(new_path1, frequencies) or not is_word_accepted(new_path2,
                                                                               frequencies) or new_path2 == new_path1:
        counter += 1
        new_path1, new_path2 = cross_over(path1, path2)
    return new_path1, new_path2


def swap(s, indexes):
    i, j = indexes
    lst = list(s)
    lst[i], lst[j] = lst[j], lst[i]
    return ''.join(lst)


def get_free_symbols(path, frequencies):
    free_symbols = copy.deepcopy(frequencies)
    c1_dict = build_frequency_dictionary(path)
    for symbol in c1_dict:
        free_symbols[symbol] -= c1_dict[symbol]
        if free_symbols[symbol] == 0:
            free_symbols.pop(symbol)
    print(free_symbols)
    return free_symbols


def random_extend(child1, free_symbols):
    random_key, random_value = random.choice(list(free_symbols.items()))
    index1 = np.random.randint(0, len(child1))
    return child1[:index1] + random_key + child1[index1:]


def mutate(child1, frequencies):
    free_symbols = get_free_symbols(child1, frequencies)
    if len(free_symbols) > 0 and random.uniform(0, 1) > 0.2:
        try:
            free_symbols.get('s')
            print(child1 + 's')
            mutated = child1 + 's'
        except KeyError:
            mutated = random_extend(child1, free_symbols)
            free_symbols = get_free_symbols(mutated, frequencies)
            if len(free_symbols) > 0 and random.uniform(0, 1) > 0.4:
                mutated = random_extend(mutated, get_free_symbols(mutated, frequencies))
    else:
        mutated = swap(child1, random.sample(range(0, len(child1)), 2))
    return mutated


def controlled_mutation(child1, frequencies):
    mutated = mutate(child1, frequencies)
    while not is_word_accepted(mutated, frequencies):
        mutated = mutate(child1, frequencies)
    print(mutated)
    return mutated


def genetic_algorithm(t, n, s, letters, weights, words):
    end_time = get_current_time() + get_millis(t)
    P = words
    multiset_dictionary = build_letter_dictionary(letters, weights)
    frequencies = build_frequency_dictionary(letters)
    best = get_maximal_in(P, multiset_dictionary)
    while get_current_time() <= end_time:
        print(P)
        best = get_maximal_in(P, multiset_dictionary)
        Q = []
        for i in range(int(len(P) / 2)):
            Pa, Pb = select_parents(P, multiset_dictionary)
            print(Pa, Pb)
            Ca, Cb = two_point_crossover(Pa, Pb, frequencies)
            print(Ca, Cb)
            Q.append(controlled_mutation(Ca, frequencies))
            Q.append(controlled_mutation(Cb, frequencies))
        P = Q
    return best


def main():
    print(is_in_dict('AAB'))
    t, n, s, letters, weights, words = read_data('tests/t2')
    print(t, n, s)
    print(words)
    result = genetic_algorithm(t, n, s, letters, weights, words)
    print(result)


main()
