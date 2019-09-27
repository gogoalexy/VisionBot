import ctypes
import sys

libc = ctypes.CDLL("libc.so.6")
libiq = ctypes.CDLL("./libiq-network.so")
libiz = ctypes.CDLL("./libiz-network.so")
print(libiq)

class iqnet(object):
    def __init__(self):
        libiq.iq_network_new.argtypes = None
        libiq.iq_network_new.restype = ctypes.c_void_p

        libiq.iq_network_set_neurons.argtypes = [ctypes.c_void_p]
        libiq.iq_network_set_neurons.restype = ctypes.c_int

        libiq.iq_network_get_weight.argtypes = [ctypes.c_void_p]
        libiq.iq_network_get_weight.restype = ctypes.c_int

        libiq.iq_network_num_neurons.argtypes = [ctypes.c_void_p]
        libiq.iq_network_num_neurons.restype = ctypes.c_int

        libiq.iq_network_send_synapse.argtypes = [ctypes.c_void_p]
        libiq.iq_network_send_synapse.restype = ctypes.c_void_p

        libiq.iq_network_set_biascurrent.argtypes = [ctypes.c_void_p, ctypes.c_int, ctypes.c_int]
        libiq.iq_network_set_biascurrent.restype = ctypes.c_void_p

        libiq.iq_network_potential.argtypes = [ctypes.c_void_p, ctypes.c_int]
        libiq.iq_network_potential.restype = ctypes.c_int

        self.obj = libiq.iq_network_new()

    def set_neurons(self):
        return libiq.iq_network_set_neurons(self.obj)
    
    def get_weight(self):
        return libiq.iq_network_get_weight(self.obj)

    def num_neurons(self):
        return libiq.iq_network_num_neurons(self.obj)

    def send_synapse(self):
        return libiq.iq_network_send_synapse(self.obj)

    def set_biascurrent(self, neuron_index, biascurrent):
        return libiq.iq_network_set_biascurrent(self.obj, neuron_index, biascurrent)

    def potential(self, neuron_index):
        return libiq.iq_network_potential(self.obj, neuron_index)

class iznet(object):
    def __init__(self):
        libiz.iz_network_new.argtypes = None
        libiz.iz_network_new.restype = ctypes.c_void_p

        libiz.iz_network_set_neurons.argtypes = [ctypes.c_void_p]
        libiz.iz_network_set_neurons.restype = ctypes.c_int

        libiz.iz_network_get_weight.argtypes = [ctypes.c_void_p]
        libiz.iz_network_get_weight.restype = ctypes.c_int

        libiz.iz_network_num_neurons.argtypes = [ctypes.c_void_p]
        libiz.iz_network_num_neurons.restype = ctypes.c_int

        libiz.iz_network_send_synapse.argtypes = [ctypes.c_void_p]
        libiz.iz_network_send_synapse.restype = ctypes.c_void_p

        libiz.iz_network_set_biascurrent.argtypes = [ctypes.c_void_p, ctypes.c_int, ctypes.c_int]
        libiz.iz_network_set_biascurrent.restype = ctypes.c_void_p

        libiz.iz_network_potential.argtypes = [ctypes.c_void_p, ctypes.c_int]
        libiz.iz_network_potential.restype = ctypes.c_float

        libiz.iz_network_adaptive_term.argtypes = [ctypes.c_void_p, ctypes.c_int]
        libiz.iz_network_adaptive_term.restype = ctypes.c_float
        
        self.obj = libiz.iz_network_new()

    def set_neurons(self):
        return libiz.iz_network_set_neurons(self.obj)
    
    def get_weight(self):
        return libiz.iz_network_get_weight(self.obj)

    def num_neurons(self):
        return libiz.iz_network_num_neurons(self.obj)

    def send_synapse(self):
        return libiz.iz_network_send_synapse(self.obj)

    def set_biascurrent(self, neuron_index, biascurrent):
        return libiz.iz_network_set_biascurrent(self.obj, neuron_index, biascurrent)

    def potential(self, neuron_index):
        return libiz.iz_network_potential(self.obj, neuron_index)
    
    def adaptive_term(self, neuron_index):
        return libiz.iz_network_adaptive_term(self.obj, neuron_index)

network = iznet()
print(network.num_neurons())
network.set_biascurrent(0,2)
network.set_biascurrent(1,2)
for i in range (0,2000):
    network.send_synapse();
    print(network.potential(0))
network.set_biascurrent(0,0)
network.set_biascurrent(1,0)
for i in range (0,1000):
    network.send_synapse();
    print(network.potential(0))
print("OK?")

