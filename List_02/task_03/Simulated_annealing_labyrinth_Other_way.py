
def follow_way(board, x, y, path):
    """Follower"""
    step = 0
    endX, endY = x, y
    for d in path:
        step += 1
        if d == 'U':
            endY -= 1
        elif d == 'D':
            endY += 1
        elif d == 'R':
            endX += 1
        else:
            endX -= 1
        if board[endY][endX] == 1:
            return path[:step - 1]
        elif board[endY][endX] == 8:
            print('sukces')
            return False


def simulated_annealing_subs(t, b, T0, graph, n, m):
    """Simulate annealing based on subs"""
    startTime = int(round(time.time() * 1000))
    endTime = startTime + t * 1000
    T = T0
    x0, y0 = find_initial_position(b)
    state = initial_solution(b, x0, y0)
    cost = len(state)
    states, costs = [state], [cost]
    all_costs = [cost]
    step = 1
    path_counter = 1
    while int(round(time.time() * 1000)) <= endTime and T > 0:
        step += 1
        T += 0.9
        if path_counter == len(state) - 2:
            path_counter = 1
        current_path = state[:path_counter]
        r_p = random_path(n, m)
        while follow_way(b, x0, y0, r_p):
            current_path.append(follow_way(b, x0, y0, r_p))
            r_p = random_path(n, m)
            print('kraze')
        path_counter += 1
        new_cost = len(current_path)
        if acceptance_probability(cost, new_cost, T) > rn.random():
            state, cost = current_path, new_cost
            if costs[len(costs) - 1] > cost:
                print('new cost')
                states.append(state)
                costs.append(cost)
    if graph:
        plot_graph(all_costs)
    return costs[len(costs) - 1], states[len(states) - 1]


def remove_sub(path):
    if len(path) > 5:
        asStr = ''.join(path)
        k = random.randint(0, 3)
        i = random.randint(1, len(path) - 1 - k)
        res = asStr[:i].join(asStr[i + k:])
    else:
        res = path
    return remove_constant_points(list(res))


def simulated_annealing_dels(t, b, T0, graph):
    """Simulated annealing based on deletion"""
    # Find end time
    startTime = int(round(time.time() * 1000))
    endTime = startTime + t * 1000
    T = T0
    x0, y0 = find_initial_position(b)
    state = initial_solution(b, x0, y0)
    print(state)
    cost = len(state)
    states, costs = [state], [cost]
    all_costs = [cost]
    step = 1
    while int(round(time.time() * 1000)) <= endTime and T > 0:
        step += 1
        T = T * 0.99
        new_state = remove_sub(state)
        while not check_way(b, x0, y0, new_state):
            new_state = remove_sub(state)
        print('wychodze')
        new_cost = len(new_state)
        if acceptance_probability(cost, new_cost, T) > rn.random():
            print('mijam')
            state, cost = new_state, new_cost
            if costs[len(costs) - 1] > cost:
                print('new')
                states.append(state)
                costs.append(cost)
            if cost not in all_costs:
                all_costs.append(cost)
    # plot costs
    if graph:
        plot_graph(all_costs)
    return costs[len(costs) - 1], states[len(states) - 1]

