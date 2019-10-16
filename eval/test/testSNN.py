import sys
import time
sys.path.append("../")
import snn

start = time.time()

net = snn.initNet()
snn.run(net, 2000)
print(snn.getPotential(net, 3))

end = time.time()
print("Consumed: {} s, {} ms per step".format(end-start, (end-start)*1000/5000))

