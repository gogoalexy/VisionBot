import sys
sys.path.append("iq-neuron")
import iqif

class SNN:
    def __init__(self, useIzModel=False, thread=1):
        if useIzModel:
            self.network = iqif.iznet()
            self.numNeurons = self.network.num_neurons()
        else:
            self.network = iqif.iqnet()
            self.network.set_num_threads(thread)
            self.numNeurons = self.network.num_neurons()

    def stimulate(self, neuronID, current):
        self.network.set_biascurrent(neuronID, current)

    def stimulateInOrder(self, input):
        for neuronID, current in enumerate(input, start=0):
            self.network.set_biascurrent(neuronID, current)

    def run(self, steps):
        for step in range(0, steps):
            self.network.send_synapse()

    def getMostActiveNeuron(self):
        activity = []
        for index in range(0, self.numNeurons):
            activity.append(self.getSpikeCount(index))
            argmax = max(zip(activity, range(len(activity))))[1]
        return argmax

    def getPotential(self, neuronID):
        return self.network.potential(neuronID)

    def getSpikeCount(self, neuronID):
        return self.network.spike_count(neuronID)

    def getFiringRate(self, neuronID):
        return self.network.spike_rate(neuronID)
