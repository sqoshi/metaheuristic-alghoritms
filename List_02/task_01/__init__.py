import signal
import sys


#################################################################
###################### Time Limitation ##########################
#################################################################
class TimedOutExc(Exception):
    pass


def deadline(timeout, *args):
    def decorate(f):
        def handler(signum, frame):
            raise TimedOutExc()

        def new_f(*args):
            signal.signal(signal.SIGALRM, handler)
            signal.alarm(timeout)
            return f(*args)
            signal.alarm(0)

        new_f.__name__ = f.__name__
        return new_f

    return decorate


#################################################################
######################## Main Problem ###########################
#################################################################
@deadline(t)
def simulated_annealing(t):
    while 1:
        print('Simulated annealing')


def main(args):
    print(args)
    simulated_annealing()


main(sys.argv)
