import copy
import random
import time

import numpy as np


####################################################################################
############################## Data Reading ########################################
####################################################################################

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


dict_set = set()


def read_dictionary():
    with open('dict') as f:
        line = f.readline()
        while line:
            try:
                dict_set.add(line.split()[0].lower())
            except:
                print(line)
            line = f.readline()
    return dict_set


dict_set = read_dictionary()


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
    if word in dict_set:
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


def cross_over(path1, path2):
    """Mixing our genotypes."""
    l1, l2 = len(path1), len(path2)
    try:
        c1, d1 = np.random.randint(0, l1 - 1), np.random.randint(0, l1 - 1)
        c2, d2 = np.random.randint(0, l2 - 1), np.random.randint(0, l2 - 1)
    except ValueError:
        c1, d1, c2, d2 = 0, 0, 0, 0
    if c1 > d1:
        c1, d1 = d1, c1
    if c2 > d2:
        c2, d2 = d2, c2
    return path1[:c1] + path2[c2:d2] + path1[d1:], path2[:c2] + path1[c1:d1] + path1[d2:]


def two_point_crossover(path1, path2, frequencies):
    """Controls that our new paths are correct."""
    new_path1, new_path2 = cross_over(path1, path2)
    step = 0
    while not is_word_accepted(new_path1, frequencies) \
            or not is_word_accepted(new_path2, frequencies) \
            or new_path2 == new_path1:
        step += 1
        if step == 2e3:
            return path1, path2
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
    return free_symbols


def random_extend(child1, free_symbols):
    random_key, random_value = random.choice(list(free_symbols.items()))
    index1 = np.random.randint(0, len(child1))
    return child1[:index1] + random_key + child1[index1:]


def mutate(child1, frequencies):
    free_symbols = get_free_symbols(child1, frequencies)
    if len(free_symbols) > 0 and random.uniform(0, 1) > 0.2:
        try:
            if 0.5 > random.uniform(0, 1):
                raise KeyError
            free_symbols.get('s')
            mutated = child1 + 's'
        except KeyError:
            try:
                free_symbols.get('d')
                mutated = child1 + 'd'
            except KeyError:
                mutated = random_extend(child1, free_symbols)
                free_symbols = get_free_symbols(mutated, frequencies)
                if len(free_symbols) > 0:
                    for _ in range(random.randint(1, len(free_symbols))):
                        mutated = random_extend(mutated, get_free_symbols(mutated, frequencies))
    else:
        if len(child1) > 2:
            mutated = swap(child1, random.sample(range(0, len(child1)), 2))
        else:
            mutated = child1
    return mutated


def controlled_mutation(child1, frequencies):
    mutated = mutate(child1, frequencies)
    step = 1
    while not is_word_accepted(mutated, frequencies):
        step += 1
        if step == 2e2: return child1
        mutated = mutate(child1, frequencies)
    return mutated


def convert_to_list(dictionary):
    result_list = []
    for key, val in dictionary.items():
        result_list.extend([key] * val)
    return result_list


print(convert_to_list({'a': 3, 'b': 4}))


def random_word_prefix(child, frequencies):
    random_prefix = child[:random.randint(0, len(child) - 1)]
    free = get_free_symbols(random_prefix, frequencies)
    free_characters = convert_to_list(free)
    random_length = random.randint(0, len(free_characters))
    _symbols = []
    for _ in range(random_length):
        x = random.choice(free_characters)
        _symbols.append(x)
        free_characters.remove(x)
    word = random_prefix + ''.join(_symbols)
    return word


def mutate_prefix(child, frequencies):
    word = random_word_prefix(child, frequencies)
    while not is_word_accepted(word, frequencies):
        word = random_word_prefix(child, frequencies)
    return word


def control(population, dictionary, max_size=16):
    population = list(dict.fromkeys(population))
    for population in population:
        if not is_in_dict(population) or len(population) <= 3:
            population.remove(population)
    probs = get_probabilities(population, dictionary)
    while len(population) > max_size:
        try:
            population.remove(population[probs.index(max(probs))])
        except IndexError:
            break
    return population


def genetic_algorithm(t, n, s, letters, weights, words):
    end_time = get_current_time() + get_millis(t)
    population = words
    multiset = build_letter_dictionary(letters, weights)
    frequencies = build_frequency_dictionary(letters)
    global_best = get_maximal_in(population, multiset)
    history = [global_best]
    while get_current_time() <= end_time:
        local_best = get_maximal_in(population, multiset)
        Q = []
        for i in range(int(len(population) / 2)):
            Pa, Pb = select_parents(population, multiset)
            Ca, Cb = two_point_crossover(Pa, Pb, frequencies)
            Q.append(controlled_mutation(Ca, frequencies))
            Q.append(controlled_mutation(Cb, frequencies))
        population.extend(Q)
        population = control(population, multiset)
        if quality(local_best, multiset) > quality(global_best, multiset):
            global_best = local_best
            history.append(global_best)
    print(history)
    print([quality(x, multiset) for x in history])
    return global_best


def main():
    t, n, s, letters, weights, words = read_data('tests/t2')
    print(t, n, s)
    print(words)
    result = genetic_algorithm(t, n, s, letters, weights, words)
    print(result)


main()
