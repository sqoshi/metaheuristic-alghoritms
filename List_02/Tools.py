import smtplib
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
