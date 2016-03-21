from count import countdown
from threading import Thread
import time


COUNT = 100000000

start1 = time.time()
countdown(COUNT)
end1 = time.time()

print "Non-threaded took %f s" % (end1 - start1)

start2 = time.time()
t1 = Thread(target=countdown,args=(COUNT//2,))
t2 = Thread(target=countdown,args=(COUNT//2,))
t1.start(); t2.start()
t1.join(); t2.join()
end2 = time.time()

print "Threaded took %f s" % (end2 - start2)
