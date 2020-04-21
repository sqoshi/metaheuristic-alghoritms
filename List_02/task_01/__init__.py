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
    sum_of_squares = math.sqrt(sum([pow(xi, 2) for xi in x]))
    return 1 - (math.cos(2 * math.pi * sum_of_squares)) + 0.1 * sum_of_squares


def random_neighbour(x):
    neighbour = []
    for xi in x:
        e = 0.5
        k = rn.randint(-5, 5)
        neighbour.append(xi + k * e)
    return neighbour


def acceptance_probability(cost, new_cost, temp):
    if new_cost < cost:
        return 1
    else:
        p = np.exp(- (new_cost - cost) / temp)
        return p


def temperature(fraction):
    return max(0.01, min(1, 1 - fraction))


def simulated_annealing(t, start, T):
    startTime = int(round(time.time() * 1000))
    endTime = startTime + t * 1000
    state = start
    cost = salomon(state)
    states, costs = [state], [cost]
    step = 1
    while int(round(time.time() * 1000)) <= endTime and T > 0:
        step += 1
        T = T * 0.99
        new_state = random_neighbour(state)
        new_cost = salomon(new_state)
        if acceptance_probability(cost, new_cost, T) > rn.random():
            state, cost = new_state, new_cost
            if costs[len(costs) - 1] > cost:
                states.append(state)
                costs.append(cost)
    plot_graphs(states, costs)
    print(states, costs)
    return min(costs), states, costs


def main(args):
    # duration = int(args.split()[0]) * pow(10, 3)  # in millis
    # x = [int(i) for i in args.split()[1:]]
    minimal, states, costs = simulated_annealing(10, [rn.randint(-100, 100) for _ in range(4)], 100)
    print(minimal)


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
