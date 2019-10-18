# Integer Quadratic Integrate-and-Fire Neuron

## Buildtime Dependencies:

* gcc (C++11)

* OpenMP >= 4.5

* cmake >= 3.9

## Compiling & Running:

```bash
mkdir build && cd build
cmake ..
make
python ../iqif.py
```

You can change the synaptic weights in the [Connection Table](inputs/Connection_Table_IQIF.txt). The numbers in each lines are `pre-synapse neuron index, post-synapse neuron index, weight, time constant` respectively.

You can change the neuron parameters in the [neuron parameter file](inputs/neuronParameter_IQIF.txt). The parameters in each lines are `neuron index, rest potential, threshold potential, reset potential, noise strength` respectively.

Currently the synaptic weights and neuron parameters CANNOT be changed during runtime session. Sorry.

I also have an [Izhikevich model](include/iz_network.h) for comparison. It is the same as IQIF ones.

You can import the library using `iqif.py` by

```python
import iqif
```
.

