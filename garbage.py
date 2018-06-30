def wait(msg):  # Loading animation
    from threading import Thread

    def animation(m):
        from time import sleep
        from itertools import cycle
        from sys import stdout
        for c in cycle('-/|\\'):
            stdout.write("%s %s\r" % (m, c))
            stdout.flush()
            sleep(0.2)
        stdout.write('\rDone!     ')
        stdout.flush()
    Thread(target=animation, args=(msg,)).start()
