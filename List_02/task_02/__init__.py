import copy
import math
import itertools
import random


def get_rectangle(x, y, board):
    value = board[y][x]
    up, down, right, left = y, y, x, x
    while board[up][x] == value and up != 0:
        if board[up][x] != value:
            break
        up -= 1
    while board[down][x] == value and down != len(board) - 1:
        if board[down][x] != value:
            break
        down += 1
    while board[y][left] == value and left != 0:
        if board[y][left] != value:
            break
        left -= 1
    while board[y][right] == value and right != len(board[y]) - 1:
        if board[y][right] != value:
            break
        right += 1
    if right != len(board[y]) - 1:
        right -= 1
    if down != len(board) - 1:
        down -= 1
    if up != 0:
        up += 1
    if left != 0:
        left += 1
    return [left, up], [right, down]


def get_all_rectangles(board):
    rectangles = []
    for i in range(0, len(board)):
        for j in range(0, len(board[i])):
            rect = get_rectangle(j, i, board)
            if rect not in rectangles:
                rectangles.append(rect)
    return rectangles


def is_any_dividable(k, board):
    rectangles = get_all_rectangles(board)
    for rect in rectangles:
        lu = rect[0]
        rd = rect[1]
        if abs(lu[0] - rd[0]) >= 2 * k + 1:
            return rect
        if abs(lu[1] - rd[1]) >= 2 * k + 1:
            return rect
    return False


def divide(k, rect, board):
    lu, rd = rect
    if abs(lu[0] - rd[0]) >= 2 * k + 1:
        new_rd = rd[0] - k - 1, rd[1]
        set_color(lu, new_rd, board, random.choice([0, 32, 64, 128, 160, 192, 223, 255]))
    elif abs(lu[1] - rd[1]) >= 2 * k + 1:
        new_rd = rd[0], rd[1] - k - 1
        set_color(lu, new_rd, board, random.choice([0, 32, 64, 128, 160, 192, 223, 255]))


def is_rectangle_right(board, rect):
    lu, rd = rect
    value = board[lu[1] + 1][lu[0] + 1]
    for i in range(lu[1], rd[1]):
        for j in range(lu[0], rd[0]):
            if board[i][j] != value:
                return False
    return True


def repair(board, rectangles):
    for lu, rd in rectangles:
        set_color(lu, rd, board, board[lu[1]][lu[0]])


def is_any_wrong(board):
    for r in get_all_rectangles(board):
        z = is_rectangle_right(board, r)
        if not z:
            return True
    return False


def division(b, k, board):
    while not is_any_dividable(k, board) is False:
        divide(k, is_any_dividable(k, board), board)
    repair(board, get_all_rectangles(board))
    while is_any_wrong(board) is True:
        board = copy.deepcopy(b)
        while not is_any_dividable(k, board) is False:
            divide(k, is_any_dividable(k, board), board)
        repair(board, get_all_rectangles(board))


########################################################################################
def compute_distance(A, B):
    if len(A) != len(B) or len(A[1]) != len(B[1]):
        raise IndexError
    n = len(A)
    m = len(A[1])
    distance = 0
    for i in range(n):
        for j in range(m):
            distance += pow((A[i][j] - B[i][j]), 2)
    return distance


def read_data():
    t, n, m, k = [int(x) for x in input().split()]
    M = []
    for i in range(n):
        z = list(input())
        M.append([int(x) for x in z if x != '\n' and x != ' '])
    return t, n, m, k, M


def read_data_from_file(file):
    f = open(file, 'r')
    t, n, m, k = [int(x) for x in f.readline().split()]
    M = [[int(num) for num in line.split()] for line in f]
    f.close()
    return t, n, m, k, M


def printM(M):
    print('\n'.join([''.join(['{:4}'.format(item) for item in row])
                     for row in M]))
    print()


def set_color_avg(left_up, right_down, M):
    value = select_zoom_value(get_average(left_up, right_down, M))
    x1, y1 = left_up
    x2, y2 = right_down
    for y in range(y1, y2 + 1):
        for x in range(x1, x2 + 1):
            M[y][x] = value


def set_color(left_up, right_down, M, value):
    x1, y1 = left_up
    x2, y2 = right_down
    for y in range(y1, y2 + 1):
        for x in range(x1, x2 + 1):
            M[y][x] = value


def select_zoom_value(avg):
    values = [0, 32, 64, 128, 160, 192, 223, 255]
    closest = lambda num, collection: min(collection, key=lambda x: abs(x - num))
    return closest(avg, values)


def get_average(left_up, right_down, M):
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
    board = copy.deepcopy(M)
    r1, r2 = math.floor(m / k), math.floor(n / k)
    rows = [i * k - 1 for i in range(1, r2)]
    columns = [i * k - 1 for i in range(1, r1)]
    rows.append(n - 1)
    columns.append(m - 1)
    right_down_all = [[x, y] for x, y in itertools.product(columns, rows)]  # wierzcholek jest w kwadracie
    left_up_all = get_left_up_all(n, m, k, right_down_all)
    for i in range(len(right_down_all)):
        set_color_avg(left_up_all[i], right_down_all[i], board)
    return board, left_up_all, right_down_all


def get_area(left_up, right_down):
    return (right_down[0] - left_up[0] + 1) * (right_down[1] - left_up[1] + 1)


def get_areas_all(left_up_all, right_down_all):
    return [(right_down_all[i][0] - left_up_all[i][0] + 1)
            * (right_down_all[i][1] - left_up_all[i][1] + 1) for
            i in range(0, len(right_down_all))]


def get_vertexes(lu, rd):
    x1, y1 = lu
    x2, y2 = rd
    # LU RU LD RD
    return [x1, y1], [x2, y1], [x1, y2], [x2, y2]


def test_areas(board, left_up_all, right_down_all):
    b = copy.deepcopy(board)
    i = 0
    while i < 9:
        set_color(left_up_all[i], right_down_all[i], b, i)
        i += 1
    printM(b)


def change_random_rectangle_color(b, rectangles):
    value = random.choice([0, 32, 64, 128, 160, 192, 223, 255])
    to_change = random.choice(rectangles)
    lu, rd = to_change
    set_color(lu, rd, b, value)


def check_left(rectangles, rect, k):
    print('----------checking left------------')
    concrete_lu, concrete_rd = rect
    left_x, up_y = concrete_lu
    right_x, down_y = concrete_rd
    for r in rectangles:
        lu, rd = r
        l_x, u_y = lu
        r_x, d_y = rd
        if up_y == u_y and down_y == d_y and r != rect and (left_x == r_x + 1) and \
                abs(l_x - r_x) + 1 > k:
            print(r)


def check_right(rectangles, rect, k):
    print('----------checking right------------')
    lu, rd = rect
    left_x, up_y = lu
    right_x, down_y = rd
    for r in rectangles:
        lu_temp, rd_temp = r
        l_x, u_y = lu_temp
        r_x, d_y = rd_temp
        if up_y == u_y and down_y == d_y and r != rect and (right_x == l_x - 1) and \
                abs(l_x - r_x) + 1 > k:
            print(r)


def check_upper(rectangles, rect, k):
    print('----------checking upper------------')
    concrete_lu, concrete_rd = rect
    left_x, up_y = concrete_lu
    right_x, down_y = concrete_rd
    for r in rectangles:
        lu, rd = r
        l_x, u_y = lu
        r_x, d_y = rd
        if left_x == l_x and right_x == r_x and r != rect and (up_y == d_y + 1) and \
                abs(u_y - d_y) + 1 > k:
            print(r)


def check_down(rectangles, rect, k):
    print('----------checking down------------')
    concrete_lu, concrete_rd = rect
    left_x, up_y = concrete_lu
    right_x, down_y = concrete_rd
    for r in rectangles:
        lu, rd = r
        l_x, u_y = lu
        r_x, d_y = rd
        if left_x == l_x and right_x == r_x and r != rect and (down_y == u_y - 1) and \
                abs(u_y - d_y) + 1 > k:
            print(r)


def main():
    t, n, m, k, M = read_data_from_file('tests/t1')
    b, left_up_all, right_down_all = init_abstract_net(n, m, k + 1, M)
    rectangles = [[left_up_all[i], right_down_all[i]] for i in range(0, len(right_down_all))]
    print(len(rectangles))
    printM(b)
    change_random_rectangle_color(b, rectangles)
    change_random_rectangle_color(b, rectangles)
    change_random_rectangle_color(b, rectangles)
    change_random_rectangle_color(b, rectangles)
    printM(b)
    print(rectangles)
    print(get_areas_all(left_up_all, right_down_all))
    z = random.choice(rectangles)
    print(z)
    check_down(rectangles, z, k)
    check_upper(rectangles, z, k)
    check_right(rectangles, z, k)
    check_left(rectangles, z, k)


main()
