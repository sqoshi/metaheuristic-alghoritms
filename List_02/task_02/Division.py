########################################################################################
################################## Division ############################################
########################################################################################
import copy
import random

from task_02 import set_color, printM


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
################################## Tests ###############################################
########################################################################################
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


########################################################################################
################################## Area's ##############################################
########################################################################################
def get_area(left_up, right_down):
    """Computes area of given block."""
    return (right_down[0] - left_up[0] + 1) * (right_down[1] - left_up[1] + 1)


def get_areas_all(left_up_all, right_down_all):
    """Computes all blocks'a area in board."""
    return [(right_down_all[i][0] - left_up_all[i][0] + 1)
            * (right_down_all[i][1] - left_up_all[i][1] + 1) for
            i in range(0, len(right_down_all))]
