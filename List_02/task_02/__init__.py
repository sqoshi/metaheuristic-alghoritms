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
    print('\n'.join([''.join(['{:5}'.format(item) for item in row])
                     for row in M]))


def main():
    t, n, m, k, M = read_data_from_file('tests/t1')
    print(t, n, m, k)
    printM(M)


main()
