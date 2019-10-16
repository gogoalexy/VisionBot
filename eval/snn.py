import sys
sys.path.append("iq-neuron")
import iqif

class SNN:
    def __init__(self):
        self.network = iqif.iqnet()
        print("Neurons: {}".format(self.network.num_neurons()))
        self.network.set_biascurrent(0,4)
        self.network.set_biascurrent(1,4)
        self.network.set_biascurrent(2,4)
        self.network.set_biascurrent(3,4)
        self.network.set_biascurrent(4,4)
        self.network.set_biascurrent(5,4)
        self.network.set_biascurrent(6,4)
        self.network.set_biascurrent(7,4)

    def run(self, steps):
        for step in range(0, steps):
            self.network.send_synapse()

    def getMostActiveNeuron(self):
        activity = []
        for index in range(0, 8):
            activity.append(self.getSpikeCount(index))
            argmax = max(zip(activity, range(len(activity))))[1]
        return argmax

    def getPotential(self, neuronID):
        return self.network.potential(neuronID)

    def getSpikeCount(self, neuronID):
        return self.network.spike_count(neuronID)
        
    def getFiringRate(self, neuronID):
        return self.network.spike_rate(neuronID)
