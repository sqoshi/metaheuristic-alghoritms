import time
import math
import random
import sys
import smtplib
import ray as ray
from runpy import run_path


def sendMail(to, file):
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login('luzneporty25@gmail.com', open('/home/piotr/Music/music/mp3.txt', 'r').read())
    from_mail = 'luzneporty25@gmail.com'
    body = (open(file, "r").read())
    message = ("From: %s\r\n" % from_mail + "To: %s\r\n" % to + "Subject: %s\r\n" % '' + "\r\n" + body)
    server.sendmail(from_mail, to, message)


#################################################################
######################## Main Problem ###########################
#################################################################

def salomon(x):
    sum_of_squares = (math.sqrt(sum([pow(xi, 2) for xi in x])))
    return 1 - (math.cos(2 * math.pi * sum_of_squares)) + 0.1 * sum_of_squares


def generate_neighbour(x):
    e = 0.01
    n = []
    for i in range(len(x)):
        k = random.randint(-5, 5)  # (random.uniform(-1, 1))
        n.append((x[i] + k * e))
    return n


def acceptanceProbability(energy, newEnergy, temperature):
    if newEnergy < energy:
        return 1.0
    return math.exp((energy - newEnergy) / temperature)


def simulated_annealing(t, x0, resets):
    startTime = int(round(time.time() * 1000))
    endTime = startTime + t
    x = x0
    fx = salomon(x)
    best = [x, fx]
    T0 = 300
    T = T0
    i = 1
    c = 0.005
    while int(round(time.time() * 1000)) <= endTime and T > 0:
        print(T, fx, x)
        i += 1
        neighbour = generate_neighbour(x)
        fx, fn = salomon(x), salomon(neighbour)
        delta = fn - fx
        r = random.uniform(0, 1.0)
        prob = math.exp(-delta / T)
        if prob > r:
            fx = fn
            x = neighbour
        T = (1 - c) * T
        if fx < best[1]:
            best[1] = fx
            best[0] = x
    return best


def main(args):
    duration = int(args.split()[0]) * pow(10, 3)  # in millis
    x = [int(i) for i in args.split()[1:]]
    print(simulated_annealing(duration, x, False))


main(input())
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
