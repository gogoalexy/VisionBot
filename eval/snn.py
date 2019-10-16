import sys
sys.path.append("iq-neuron")
import iqif

def initNet():
    network = iqif.iqnet()
    print("Neurons: {}".format(network.num_neurons()))
    network.set_biascurrent(0,4)
    network.set_biascurrent(1,4)
    return network

def run(network, steps):
    for step in range(0, steps):
        network.send_synapse()
        print( "0: {}, 1: {}, 2: {}, 3: {}, 4: {}, 5: {}, 6: {}, 7: {}".format(network.potential(0),
        network.potential(1), network.potential(2), network.potential(3), network.potential(4),
        network.potential(5), network.potential(6), network.potential(7)) )

def getPotential(network, neuronID):
    return network.potential(neuronID)
