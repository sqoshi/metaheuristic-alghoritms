import copy
import random
import time

import numpy as np


def read_dictionary(frequencies):
    dict_set = set()
    correct_set = set()
    with open('../dict') as f:
        line = f.readline()
        while line:
            try:
                word = line.split()[0].lower()
                dict_set.add(word)
                if are_frequencies_right(word, frequencies):
                    correct_set.add(word)
            except:
                print(line)
            line = f.readline()
    return dict_set, correct_set


def read_data(filepath):
    c, population = [], []
    words = []
    f = open(filepath, "r")
    line = f.readline()
    t, n, s = [int(item) for item in line.split() if item != '\n']
    for i in range(n):
        ci, pi = f.readline().split()
        c += [ci]
        population += [int(pi)]
    for i in range(s):
        words += [f.readline().split()[0]]
    f.close()
    return t, n, s, c, population, words


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


def get_free_symbols(path, frequencies):
    free_symbols = copy.deepcopy(frequencies)
    c1_dict = build_frequency_dictionary(path)
    for symbol in c1_dict:
        free_symbols[symbol] -= c1_dict[symbol]
        if free_symbols[symbol] == 0:
            free_symbols.pop(symbol)
    return free_symbols


####################################################################################
########################### Main Algorithm #########################################
####################################################################################
def get_probabilities(population, dictionary):
    return [quality(pi, dictionary) / sum([quality(pi, dictionary) for pi in population]) for pi in population]


def select_parents(population, dictionary):
    """Selects parents with probability (quality(x_i)/sum(quality(X))"""
    random.shuffle(population)
    qualities = get_probabilities(population, dictionary)
    result = [False for _ in range(len(population))]
    while result.count(True) < 2:
        for i in range(len(result)):
            if result.count(True) == 2:
                break
            if np.random.uniform(0, 1) < qualities[i]:
                result[i] = True
    g = (i for i, e in enumerate(result) if e is True)
    i = next(g)
    j = next(g)
    return population[i], population[j]


def crossover(parent1, parent2, correct_words, multiset):
    crossed = parent1 + parent2
    available_words = []
    crossed_alphabet = build_frequency_dictionary(crossed)
    for word in correct_words:
        if are_frequencies_right(word, crossed_alphabet):
            available_words += [word]
    try:
        available_words.remove(parent1)
        available_words.remove(parent2)
    except:
        pass
    return random.choice(available_words)


def mutate(child, correct_words):
    available_words = []
    random_prefix = child[:random.randint(0, len(child) - 1)]
    for word in correct_words:
        if word.startswith(random_prefix):
            available_words.append(word)
    try:
        return random.choice(available_words)
    except:
        return child




def genetic_algorithm(t, frequencies, correct_words, initial_words, multiset):
    end_time = get_current_time() + get_millis(t)
    population = initial_words
    print(initial_words)
    global_best = get_maximal_in(population, multiset)
    while get_current_time() < end_time:
        # print(population)
        Q = []
        for _ in range(int(8)):
            parent1, parent2 = select_parents(population, multiset)
            child = crossover(parent1, parent2, correct_words, multiset)
            generation = mutate(child, correct_words)
            Q.append(generation)
        population = Q
        local_best = get_maximal_in(population, multiset)
        if quality(local_best, multiset) >= quality(global_best, multiset):
            global_best = local_best
            print(global_best)
    return global_best, quality(global_best, multiset)


def main():
    t, n, s, letters, weights, initial_words = read_data('../tests/t2')
    frequencies = build_frequency_dictionary(letters)
    multiset = build_letter_dictionary(letters, weights)
    all_words, correct_words = read_dictionary(frequencies)
    path = genetic_algorithm(t, frequencies, correct_words, initial_words, multiset)
    print(path)


main()
