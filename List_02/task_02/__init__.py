from __future__ import print_function

import copy
import math
import itertools
import random
import sys

import matplotlib.pyplot as plt
import numpy as np

import sys
########################################################################################
################################# Data Section #########################################
########################################################################################
import time


def read_data():
    """Reads data from input"""
    t, n, m, k = [int(x) for x in input().split()]
    M = []
    for i in range(n):
        z = list(input())
        M.append([int(x) for x in z if x != '\n' and x != ' '])
    return t, n, m, k, M


def read_data_from_file(file):
    """Reads data from file"""
    f = open(file, 'r')
    t, n, m, k = [int(x) for x in f.readline().split()]
    M = [[int(num) for num in line.split()] for line in f]
    f.close()
    return t, n, m, k, M


########################################################################################
############################ Quality and output ########################################
########################################################################################

def compute_distance(A, B):
    """Quality function for simulated annealing"""
    if len(A) != len(B) or len(A[1]) != len(B[1]):
        raise IndexError
    n = len(A)
    m = len(A[1])
    distance = 0
    for i in range(n):
        for j in range(m):
            distance += pow((A[i][j] - B[i][j]), 2)
    return distance


def eprint(a):
    for i in range(len(a)):
        for j in range(len(a[i])):
            if j != len(a[i]) - 1:
                sys.stderr.write(str(a[i][j]))
                sys.stderr.write(" ")
            else:
                sys.stderr.write(str(a[i][j]))
        sys.stderr.write("\n")


def printM(M):
    """Formatted display"""

    print('\n'.join([''.join(['{:1}'.format(item) for item in row]) for row in M]))


########################################################################################
##################################### Colouring ########################################
########################################################################################

def set_color_avg(left_up, right_down, M):
    """Set start colors as average of elements in each block."""
    value = select_zoom_value(get_average(left_up, right_down, M))
    x1, y1 = left_up
    x2, y2 = right_down
    for y in range(y1, y2 + 1):
        for x in range(x1, x2 + 1):
            M[y][x] = value


def set_color(left_up, right_down, M, value):
    """Sets color for rectangle <lu,rd> on board M as value = value."""
    x1, y1 = left_up
    x2, y2 = right_down
    for y in range(y1, y2 + 1):
        for x in range(x1, x2 + 1):
            M[y][x] = value


########################################################################################
################## Functions mostly for initial solution ###############################
########################################################################################
def select_zoom_value(avg):
    """Selects value from list closest to the average for example avg: 217,4 result: 223"""
    values = [0, 32, 64, 128, 160, 192, 223, 255]
    closest = lambda num, collection: min(collection, key=lambda x: abs(x - num))
    return closest(avg, values)


def get_average(left_up, right_down, M):
    """Gets average of values in block"""
    avg = 0
    x1, y1 = left_up
    x2, y2 = right_down
    quantity = 0
    for y in range(y1, y2 + 1):
        for x in range(x1, x2 + 1):
            avg += M[y][x]
            quantity += 1
    return avg / quantity


def get_left_up_all(n, m, k, right_down_all):
    """Computes all left,up co-ordinates by given right down co-ordinates of all blocks."""
    k -= 1
    left_up_all = []
    for i in range(0, len(right_down_all)):
        x, y = right_down_all[i][0], right_down_all[i][1]
        y1, x1 = y - k, x - k
        if y == n - 1:
            y1 = right_down_all[i - 1][1] + 1
        if x == m - 1:
            x1 = right_down_all[i - math.floor(n / (k + 1))][0] + 1
        left_up_all.append([x1, y1])
    return left_up_all


def init_abstract_net(n, m, k, M):
    """Imposes net on board that divides our board into rectangles bigger than kxk
    Here it's implemented for k+1 to give SA chance to find neighbours by extending one area by other area cost."""
    board = copy.deepcopy(M)
    r1, r2 = math.floor(m / k), math.floor(n / k)
    rows = [i * k - 1 for i in range(1, r2)]
    columns = [i * k - 1 for i in range(1, r1)]
    rows.append(n - 1)
    columns.append(m - 1)
    right_down_all = [[x, y] for x, y in itertools.product(columns, rows)]  # vertexes are inside rectangle! lu,rd
    left_up_all = get_left_up_all(n, m, k, right_down_all)
    for i in range(len(right_down_all)):
        set_color_avg(left_up_all[i], right_down_all[i], board)
    return board, left_up_all, right_down_all


########################################################################################
###################### Neighbouring blocks validation ##################################
########################################################################################
def check_left(rectangles, rect, k):
    """Function checks if block to the left of rect meets the conditions to be reduced
    and return this block if it's proper"""
    concrete_lu, concrete_rd = rect
    left_x, up_y = concrete_lu
    right_x, down_y = concrete_rd
    for r in rectangles:
        lu, rd = r
        l_x, u_y = lu
        r_x, d_y = rd
        if up_y == u_y and down_y == d_y and r != rect and (left_x == r_x + 1) and \
                abs(l_x - r_x) + 1 > k:
            return r


def check_right(rectangles, rect, k):
    """Function checks if block to the right of rect meets the conditions to be reduced
    and return this block if it's proper"""
    lu, rd = rect
    left_x, up_y = lu
    right_x, down_y = rd
    for r in rectangles:
        lu_temp, rd_temp = r
        l_x, u_y = lu_temp
        r_x, d_y = rd_temp
        if up_y == u_y and down_y == d_y and r != rect and (right_x == l_x - 1) and \
                abs(l_x - r_x) + 1 > k:
            return r


def check_upper(rectangles, rect, k):
    """Function checks if block up on rect meets the conditions to be reduced
    and return this block if it's proper"""
    lu, rd = rect
    left_x, up_y = lu
    right_x, down_y = rd
    for r in rectangles:
        lu, rd = r
        l_x, u_y = lu
        r_x, d_y = rd
        if left_x == l_x and right_x == r_x and r != rect and (up_y == d_y + 1) and \
                abs(u_y - d_y) + 1 > k:
            return r


def check_down(rectangles, rect, k):
    """Function checks if block under rect meets the conditions to be reduced
    and return this block if it's proper"""
    concrete_lu, concrete_rd = rect
    left_x, up_y = concrete_lu
    right_x, down_y = concrete_rd
    for r in rectangles:
        lu, rd = r
        l_x, u_y = lu
        r_x, d_y = rd
        if left_x == l_x and right_x == r_x and r != rect and (down_y == u_y - 1) and \
                abs(u_y - d_y) + 1 > k:
            return r


########################################################################################
########################### Operations on rectangles ###################################
########################################################################################
def change_random_rectangle_color(b, rectangles):
    """ Changes random block's color on random color."""
    value = random.choice([0, 32, 64, 128, 160, 192, 223, 255])
    to_change = random.choice(rectangles)
    lu, rd = to_change
    set_color(lu, rd, b, value)


def find_good_one(rectangles, k):
    """Function chooses rectangle to be extended and check if his neighbours are "extendable"."""
    to_extend = random.choice(rectangles)
    environment = []
    if check_left(rectangles, to_extend, k) is not None:
        environment.append('L')
    if check_right(rectangles, to_extend, k) is not None:
        environment.append('R')
    if check_upper(rectangles, to_extend, k) is not None:
        environment.append('U')
    if check_down(rectangles, to_extend, k) is not None:
        environment.append('D')
    while len(environment) == 0:
        to_extend = random.choice(rectangles)
        if check_left(rectangles, to_extend, k) is not None:
            environment.append('L')
        if check_right(rectangles, to_extend, k) is not None:
            environment.append('R')
        if check_upper(rectangles, to_extend, k) is not None:
            environment.append('U')
        if check_down(rectangles, to_extend, k) is not None:
            environment.append('D')
    return to_extend, environment


def random_extend(rects, k):
    """ Function randomly chooses one of block and which direction of extension we are going."""
    rectangles = copy.deepcopy(rects)
    to_extend, environment = find_good_one(rectangles, k)
    pivot = random.choice(environment)
    if pivot == 'L':
        block = check_left(rectangles, to_extend, k)
        decreased_block = copy.deepcopy(block)
        extended_lu, extended_rd = to_extend[0], to_extend[1]
        extended_r, extended_d = extended_rd
        extended_l, extended_u = extended_lu
        extended_l -= 1
        block_lu, block_rd = decreased_block
        block_l, block_u = block_lu
        block_r, block_d = block_rd
        block_r -= 1
    elif pivot == 'U':
        block = check_upper(rectangles, to_extend, k)
        decreased_block = copy.deepcopy(block)
        extended_lu, extended_rd = to_extend[0], to_extend[1]
        extended_r, extended_d = extended_rd
        extended_l, extended_u = extended_lu
        extended_u -= 1
        block_lu, block_rd = decreased_block
        block_l, block_u = block_lu
        block_r, block_d = block_rd
        block_d -= 1
    elif pivot == 'R':
        block = check_right(rectangles, to_extend, k)
        decreased_block = copy.deepcopy(block)
        extended_lu, extended_rd = to_extend[0], to_extend[1]
        extended_r, extended_d = extended_rd
        extended_l, extended_u = extended_lu
        extended_r += 1
        block_lu, block_rd = decreased_block
        block_l, block_u = block_lu
        block_r, block_d = block_rd
        block_l += 1
    elif pivot == 'D':
        block = check_down(rectangles, to_extend, k)
        decreased_block = copy.deepcopy(block)
        extended_lu, extended_rd = to_extend[0], to_extend[1]
        extended_r, extended_d = extended_rd
        extended_l, extended_u = extended_lu
        extended_d += 1
        block_lu, block_rd = decreased_block
        block_l, block_u = block_lu
        block_r, block_d = block_rd
        block_u += 1
    big = [[extended_l, extended_u], [extended_r, extended_d]]
    small = [[block_l, block_u], [block_r, block_d]]
    i1 = rectangles.index(block)
    i2 = rectangles.index(to_extend)
    rectangles[i1] = small
    rectangles[i2] = big
    return rectangles


def acceptance_probability(cost, new_cost, temp):
    if new_cost < cost:
        return 1
    else:
        p = np.exp(- (new_cost - cost) / temp)
        return p


def plot_graph(costs):
    """Display graph of costs function"""
    plt.figure()
    plt.plot(costs, 'b')
    plt.title("Costs")
    plt.show()


def paint(rectangles, b):
    """Paints board by co-ordinates in rectangles list."""
    board = copy.deepcopy(b)
    for lu, rd in rectangles:
        x, y = lu[0] + 2, lu[1] + 2
        set_color(lu, rd, board, board[y][x])
    return board


def simulated_annealing(t, b, n, m, k, T0, graph):
    """Function simulate annealing"""
    board_Copy = copy.deepcopy(b)
    # Find end time.
    startTime = int(round(time.time() * 1000))
    endTime = startTime + t * 1000
    T = T0
    # Let's impose net on our board, and take co-ordinates of rectangles made by net.
    board, left_up_all, right_down_all = init_abstract_net(n, m, k + 1, board_Copy)
    rectangles = [[left_up_all[i], right_down_all[i]] for i in range(0, len(right_down_all))]
    cost = compute_distance(b, board)

    # Init our history!
    boards = [board]
    history_of_rectangles = [rectangles]
    costs = [cost]

    # Graphs Data
    all_costs = [cost]

    step = 1
    while int(round(time.time() * 1000)) <= endTime and T > 0:
        step += 1
        # Decrease time.
        T *= 0.8

        # Random neighbour choosing
        change_random_rectangle_color(board, rectangles)
        new_rectangles = random_extend(rectangles, k)
        new_board = paint(new_rectangles, board)
        change_random_rectangle_color(new_board, new_rectangles)
        change_random_rectangle_color(new_board, new_rectangles)
        new_cost = compute_distance(board, new_board)
        # We need to check if we did not extended block A by block B, which has same values.
        while new_cost == 0:
            new_rectangles = random_extend(rectangles, k)
            new_board = paint(new_rectangles, board)
            change_random_rectangle_color(new_board, new_rectangles)
            change_random_rectangle_color(new_board, new_rectangles)
            new_cost = compute_distance(board, new_board)

        if acceptance_probability(cost, new_cost, T) > random.uniform(0, 1):
            # update our candidates
            rectangles, cost, board = new_rectangles, new_cost, new_board
            # update bests.
            if cost < costs[len(costs) - 1]:
                costs.append(cost)
                history_of_rectangles.append(rectangles)
                boards.append(board)
            # Data for graph (Avoiding repetitions to make graphs more clean)
            if cost not in all_costs:
                all_costs.append(cost)
    if graph:
        plot_graph(all_costs)
    return costs[len(costs) - 1], boards[len(boards) - 1]


def main():
    # t, n, m, k, M = read_data_from_file('tests/t1')
    t, n, m, k = [int(x) for x in input().split()]
    M = [[int(x) for x in input().split()] for _ in range(n)]
    cost, board = simulated_annealing(t, M, n, m, k, 1000000, graph=False)
    print(cost)
    eprint(board)


main()
