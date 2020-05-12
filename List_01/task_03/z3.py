import copy
import random
import time


def read_data(filename):
    f = open(filename, "r")
    line = f.readline()
    t, n, m = line.split()
    line = f.readline()
    array = []
    while line:
        array.append([int(x) for x in line if x != '\n'])
        line = f.readline()
    return int(t), int(n), int(m), array


def get_distance(graph, path):
    distance = 0
    for i in range(0, len(path) - 1):
        distance += graph[path[i]][path[i + 1]]
    return distance


def get_swapped(path):
    list = path.copy()
    i = random.randint(0, len(list) - 2)
    j = random.randint(0, len(list) - 2)
    while j == i or path[i] == path[j]:
        indexes_1 = [m for m, e in enumerate(path) if e == path[i]]
        indexes_2 = [m for m, e in enumerate(path) if e != path[i]]
        # print(indexes_1)
        # print(indexes_2)
        # print(path)
        i = random.choice(indexes_1)
        j = random.choice(indexes_2)
    return remove_const_one(swap_positions(list, i, j))


def swap_positions(list, pos1, pos2):
    l = list.copy()
    l[pos1], l[pos2] = l[pos2], l[pos1]
    return l


def get_all_swaps(list):
    result = []
    for i in range(0, len(list)):
        l = copy.deepcopy(list)
        for j in range(0, len(list)):
            z = swap_positions(l, i, j)
            el = ' '.join([str(elem) for elem in z])
            if z not in result:
                result.append(z)
    return result


def get_start(b):
    board = b.copy()
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] == 5:
                return int(j), int(i)


def getNeighbours(x, y, board):
    D = board[y + 1][x]
    U = board[y - 1][x]
    L = board[y][x - 1]
    R = board[y][x + 1]
    return [U, D, L, R]


def checkMove(x, y, board):
    if board[y][x] == 0:
        return 1
    elif board[y][x] == 1:
        return -1
    else:
        return 0


def move(x, y, direction, board):
    if direction == "UP":
        if checkMove(x, y - 1, board):
            board[y][x], board[y - 1][x] = board[y - 1][x], board[y][x]
    elif direction == "DOWN":
        if checkMove(x, y + 1, board):
            board[y][x], board[y + 1][x] = board[y + 1][x], board[y][x]
    elif direction == "LEFT":
        if checkMove(x - 1, y, board):
            board[y][x], board[y][x - 1] = board[y][x - 1], board[y][x]
    elif direction == "RIGHT":
        if checkMove(x + 1, y, board):
            board[y][x + 1], board[y][x] = board[y][x], board[y][x + 1]


def get_initial(board, x, y):
    counter = 0
    path = []
    b = board.copy()
    currentX, currentY = x, y
    neighs = getNeighbours(x, y, b)
    while not neighs.__contains__(1):
        neighs = getNeighbours(currentX, currentY, b)
        if neighs[0] != 1:
            move(currentX, currentY, "UP", b)
            counter += 1
            currentY -= 1
            path.append('U')
    while neighs[0] == 1:
        neighs = getNeighbours(currentX, currentY, b)
        if neighs[0] == 8:
            return path + ['U']
        if neighs[3] != 1:
            move(currentX, currentY, "RIGHT", b)
            currentX += 1
            path.append('R')
        if neighs[3] == 1:
            break
    while neighs[3] == 1:
        neighs = getNeighbours(currentX, currentY, b)
        if neighs[3] == 8:
            return path + ['R']
        if neighs[1] != 1:
            move(currentX, currentY, "DOWN", b)
            currentY += 1
            path.append('D')
        if neighs[1] == 1:
            break
    while neighs[1] == 1:
        neighs = getNeighbours(currentX, currentY, b)
        if neighs[1] == 8:
            return path + ['D']
        if neighs[2] != 1:
            move(currentX, currentY, "LEFT", b)
            currentX -= 1
            path.append('L')
        if neighs[2] == 1:
            break
    while neighs[2] == 1:
        neighs = getNeighbours(currentX, currentY, b)
        if neighs[2] == 8:
            return path + ['L']
        if neighs[0] != 1:
            move(currentX, currentY, "UP", b)
            currentY -= 1
            path.append('U')
        if neighs[0] == 1:
            break


def is_gate_crossed(x0, y0, b, list):
    board = copy.deepcopy(b)
    currentX, currentY = x0, y0
    i = 0
    for dir in list:
        if dir == "U":
            move(currentX, currentY, "UP", board)
            currentY -= 1
        elif dir == "D":
            move(currentX, currentY, "DOWN", board)
            currentY += 1
        elif dir == "L":
            move(currentX, currentY, "LEFT", board)
            currentX -= 1
        elif dir == "R":
            move(currentX, currentY, "RIGHT", board)
            currentX += 1
        if board[currentY][currentX] == 8:
            return list[:i]
        i += 1
    return False


def is_gate_passed(x0, y0, b, list):
    board = copy.deepcopy(b)
    currentX, currentY = x0, y0
    for dir in list:
        if dir == "U":
            move(currentX, currentY, "UP", board)
            currentY -= 1
        elif dir == "D":
            move(currentX, currentY, "DOWN", board)
            currentY += 1
        elif dir == "L":
            move(currentX, currentY, "LEFT", board)
            currentX -= 1
        elif dir == "R":
            move(currentX, currentY, "RIGHT", board)
            currentX += 1
    if board[currentY][currentX] == 8:
        return True
    else:
        return False


def remove_const_one(n):
    neighbours_strings = []
    z = ''.join([el for el in n])
    while "UD" in z or "DU" in z or "LR" in z or "RL" in z:
        z = z.replace("UD", "")
        z = z.replace("DU", "")
        z = z.replace("LR", "")
        z = z.replace("RL", "")
    neighbours_strings.append(list(z))
    return list(z)


def remove_consts(neighbours):
    neighbours_strings = []
    for n in neighbours:
        z = ''.join([el for el in n])
        while "UD" in z or "DU" in z or "LR" in z or "RL" in z:
            z = z.replace("UD", "")
            z = z.replace("DU", "")
            z = z.replace("LR", "")
            z = z.replace("RL", "")
        neighbours_strings.append(list(z))
    return neighbours_strings


def tabu_search(t, board, l=50, tweak_no=20):
    end_time = int(round(time.time() * 1000)) + t * 1000
    x0, y0 = get_start(board)
    S = get_initial(board, x0, y0)
    best = S
    Tabu = [S]
    while int(round(time.time() * 1000)) < end_time:
        if len(Tabu) > l:
            Tabu.pop(0)
        R = get_swapped(S)
        for _ in range(tweak_no - 1):
            W = get_swapped(S)
            if W not in Tabu and (len(W) < len(R) or R in Tabu):
                R = W
        if R not in Tabu:
            S = R
            Tabu.append(R)
        if len(S) < len(best):
            best = S
    return best


def modern_tabu_search(t, board):
    end_time = int(round(time.time() * 1000)) + t * 1000
    x0, y0 = get_start(list(board))
    initial = get_initial(copy.deepcopy(board), x0, y0)
    best_path, best_dist = initial, len(initial)
    x = initial
    last_step = x[len(x) - 1]
    minimal_distance = best_dist
    T = []
    while int(round(time.time() * 1000)) < end_time:
        neighbours = remove_consts(get_all_swaps(x[:len(x) - 1]))
        for neigh in neighbours:
            if neigh not in T:
                sample = len(neigh)
                if sample <= minimal_distance and is_gate_passed(x0, y0, board, neigh + [last_step]):
                    minimal_distance = sample
                    x = neigh
                    x.append(last_step)
                    if best_dist >= sample:
                        best_dist = sample
                        best_path = x
                    T.append(neigh)
    return best_path


def main():
    # t, n, m = [int(x) for x in input().split()]
    # arr = []
    # for i in range(n):
    #    z = list(input())
    #    arr.append([int(x) for x in z if x != '\n'])
    # b = arr
    t, n, m, b = read_data('tests/board1')
    result = modern_tabu_search(t, b)
    r2 = tabu_search(t, b)
    print(result, len(result))
    print(r2, len(r2))


main()
