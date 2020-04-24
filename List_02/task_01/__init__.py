import time
import math
import smtplib
import numpy as np
import numpy.random as rn
import matplotlib.pyplot as plt


def sendMail(to, file):
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login('luzneporty25@gmail.com', open('/home/piotr/Music/music/mp3.txt', 'r').read())
    from_mail = 'luzneporty25@gmail.com'
    body = (open(file, "r").read())
    message = ("From: %s\r\n" % from_mail + "To: %s\r\n" % to + "Subject: %s\r\n" % '' + "\r\n" + body)
    server.sendmail(from_mail, to, message)


def plot_graphs(states, costs):
    plt.figure()
    plt.subplot(121)
    plt.plot(states, 'r')
    plt.title("States")
    plt.subplot(122)
    plt.plot(costs, 'b')
    plt.title("Costs")
    plt.show()


#################################################################
######################## Main Problem ###########################
#################################################################


def salomon(x):
    """Salomon's Function"""
    sum_of_squares = math.sqrt(sum([pow(xi, 2) for xi in x]))
    return 1 - (math.cos(2 * math.pi * sum_of_squares)) + 0.1 * sum_of_squares


def random_neighbour(x):
    """Random neighbour"""
    neigh = []
    e = 2
    for i in range(len(x)):
        neigh.append(x[i] + rn.uniform(-e, e))
    return neigh


def acceptance_probability(cost, new_cost, temp):
    # If new cost is smaller ret 1
    if new_cost < cost:
        return 1
    # Else use return p from formula e^(-delta/temperature)
    else:
        p = np.exp(- (new_cost - cost) / temp)
        return p


def simulated_annealing(t, start, T0, resets):
    # Find end time
    startTime = int(round(time.time() * 1000))
    endTime = startTime + t * 1000
    T = T0
    # set initial solution
    state = start
    cost = salomon(state)
    states, costs = [state], [cost]
    step = 1
    # while we have time and temperature is bigger than 0.
    while int(round(time.time() * 1000)) <= endTime and T > 0:
        step += 1
        # Decrease temperature
        T = T * 0.9995
        # Generate neighbour
        if resets and cost > costs[len(costs) - 1] and step % 500000 == 0:
            state, cost = states[len(states) - 1], costs[len(costs) - 1]
        new_state = random_neighbour(state)
        new_cost = salomon(new_state)
        # if probability is bigger than float from range 0,1 ( The less time  we have the less we jump to worse x)
        if acceptance_probability(cost, new_cost, T) > rn.random():
            state, cost = new_state, new_cost
            # Let's make history of our bests for example to make beautiful diagram cost/n.
            if costs[len(costs) - 1] > cost:
                states.append(state)
                costs.append(cost)
    plot_graphs(states, costs)
    return states, costs


def SA(t, x0, resets):
    startTime = int(round(time.time() * 1000))
    endTime = startTime + t * 1000
    x = x0
    best = [x, salomon(x)]
    T0 = 100
    T = T0
    i = 1
    while int(round(time.time() * 1000)) <= endTime and T > 0:
        i += 1
        if i % 500000 == 0 and fx > best[1] and resets:
            x = random_neighbour(best[0])  # [(random.randint(-10, 10)) for _ in range(4)]  # Lose
        neighbour = random_neighbour(x)
        fx, fn = (salomon(x)), (salomon(neighbour))
        if rn.uniform(0, 1.0) < acceptance_probability(fx, fn, T):
            x = neighbour
            fx = fn
        T = T * 0.99
        if fx < best[1]:
            best[1] = fx
            best[0] = neighbour
    return best


def main(args):
    # duration = int(args.split()[0])  # in seconds
    # x = [int(i) for i in args.split()[1:]]
    states, costs = simulated_annealing(30, [rn.uniform(-10, 10) for _ in range(4)], 100, False)
    print(SA(30, [rn.uniform(-10, 10) for _ in range(4)], False))
    print(states[len(states) - 1], costs[len(costs) - 1])


main("as")
# main(sys.argv[1:6])

"""
ray.init()

def resetTest(args, iterations):
    file = "out"
    f = open(file, "w+")
    duration = int(args[0]) * pow(10, 3)  # in millis
    x = [int(i) for i in args[1:]]
    w, y = [], []
    for i in range(iterations):
        ret_id1 = simulated_annealing.remote(duration, x, True)
        ret_id2 = simulated_annealing.remote(duration, x, False)
        ret1, ret2 = ray.get([ret_id1, ret_id2])
        print(ret1, ret2)
        w.append(ret1)
        y.append(ret2)
        f.write("{} {}\n".format(ret1, ret2))
    f.write("{} {} {} {}\n".format("Average With Reset =",
                                   sum(n for _, n in w) / len(w),
                                   "Average Without Reset =",
                                   sum(n for _, n in y) / len(y)))
    f.close()
    # sendMail('piotrpopis@icloud.com', file)
"""
