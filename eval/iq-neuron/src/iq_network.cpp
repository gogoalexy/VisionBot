#if defined(_WIN32) && defined(iq_network_EXPORTS)
#    define DLLEXPORTIQ __declspec (dllexport)
#else
#    define DLLEXPORTIQ
#endif

#include "iq_network.h"

using namespace std;

iq_network::iq_network()
{
    _num_neurons = linenum_neuronParameter();
    _neurons = new iq_neuron[_num_neurons];
    _tau = new int[_num_neurons * _num_neurons]();
    _f = new int[_num_neurons * _num_neurons]();
    _n = new int[_num_neurons * _num_neurons]();
    _weight = new int[_num_neurons * _num_neurons]();
    _scurrent = new int[_num_neurons * _num_neurons]();
    _ncurrent = new int[_num_neurons]();
    _biascurrent = new int[_num_neurons]();

    get_weight();
    set_neurons();
    return;
}

iq_network::~iq_network()
{
    delete[] _weight;
    delete[] _scurrent;
    delete[] _ncurrent;
    delete[] _biascurrent;
    delete[] _tau;
    delete[] _f;
    delete[] _n;
    delete[] _neurons;
    return;
}

int iq_network::linenum_neuronParameter()
{
    int i[7], linenum = 0;
    FILE *fp = fopen("iq-neuron/inputs/neuronParameter_IQIF.txt", "r");
    if(fp == NULL) {
        printf("neuronParameter_IQIF.txt file not opened\n");
        return -1;
    }

    while(fscanf(fp, " %d %d %d %d %d %d %d", &i[0], &i[1], &i[2],
            &i[3], &i[4], &i[5], &i[6]) == 7) {
        linenum++;
    }
    fclose(fp);
    return linenum;
}

int iq_network::set_neurons()
{
    int i, rest, threshold, reset, a, b, noise;
    FILE *fp;

    /*
    if(*(_tau + 0) == 0) {
        printf("synapse decay time constant _tau = %d\n", _tau);
        printf("error: please get_weight() first to set _tau.\n");
        return 1;
    }
    */
    fp = fopen("iq-neuron/inputs/neuronParameter_IQIF.txt", "r");
    while(fscanf(fp, " %d %d %d %d %d %d %d", &i, &rest, &threshold,
            &reset, &a, &b, &noise) == 7) {
        (_neurons + i)->set(rest, threshold, reset, a, b, noise);
    }
    fclose(fp);
    return 0;
}

int iq_network::get_weight()
{
    int i, j, temp, temptwo;
    FILE *fp;
    for(i = 0; i < _num_neurons; i++) {
        for(j = 0; j < _num_neurons; j++) {
            *(_scurrent + _num_neurons*i + j) = 0;
            *(_weight + _num_neurons*i + j) = 0;
            *(_tau + _num_neurons*i + j) = 0;
            *(_f + _num_neurons*i + j) = 0;
            *(_n + _num_neurons*i + j) = 0;
        }
        *(_biascurrent + i) = 0;
        *(_ncurrent + i) = 0;
    }

    fp = fopen("iq-neuron/inputs/Connection_Table_IQIF.txt", "r");
    if(fp == NULL) {
        printf("Connection_Table_IQIF.txt file not opened\n");
        return 1;
    }

    while(fscanf(fp, "%d %d %d %d", &i, &j, &temp, &temptwo) == 4) {
        *(_weight + _num_neurons*i + j) = temp;
        *(_tau + _num_neurons*i + j) = temptwo;
        if(temptwo >= 10) {
            *(_f + _num_neurons*i + j) = (int) (log10(0.9) / log10((temptwo-1)/(float) temptwo));
        }
        else {
            printf("tau[%d][%d] = %d\n", i, j, *(_tau + _num_neurons*i + j));
            printf("error: synapse time constant cannot be less than 10!\n");
            return 1;
        }
    }
    fclose(fp);
    return 0;
}

int iq_network::num_neurons()
{
    return _num_neurons;
}

void iq_network::send_synapse()
{
    /* accumulating/decaying synapse current */
    if(_num_threads > 1) {
        #pragma omp parallel
        {
            int* ncurrent_private = new int[_num_neurons]();
            #pragma omp for
            for(int i = 0; i < _num_neurons; i++) {
                int *pts = _scurrent + _num_neurons*i;
                int *ptn = _n + _num_neurons*i;
                int *ptf = _f + _num_neurons*i;
                if((_neurons + i)->is_firing()) {
                    int *ptw = _weight + _num_neurons*i;
                    for(int j = 0; j < _num_neurons; j++) {
                        *(pts + j) += *(ptw + j);
                        ncurrent_private[j] += *(pts + j);
                        if(*(ptn + j) > *(ptf + j)) {
                            *(ptn + j) = 0;
                            *(pts + j) = *(pts + j) * 9 / 10;
                        }
                        (*(ptn + j))++;
                    }
                }
                else {
                    for(int j = 0; j < _num_neurons; j++) {
                        ncurrent_private[j] += *(pts + j);
                        if(*(ptn + j) > *(ptf + j)) {
                            *(ptn + j) = 0;
                            *(pts + j) = *(pts + j) * 9 / 10;
                        }
                        (*(ptn + j))++;
                    }
                }
            }
            #pragma omp critical
            {
                for(int i = 0; i < _num_neurons; i++) {
                    *(_ncurrent + i) += ncurrent_private[i];
                }
            }
            delete[] ncurrent_private;
        }
    }
    else {
        for(int i = 0; i < _num_neurons; i++) {
            int *pts = _scurrent + _num_neurons*i;
            int *ptn = _n + _num_neurons*i;
            int *ptf = _f + _num_neurons*i;
            if((_neurons + i)->is_firing()) {
                int *ptw = _weight + _num_neurons*i;
                for(int j = 0; j < _num_neurons; j++) {
                    *(pts + j) += *(ptw + j);
                    *(_ncurrent + j) += *(pts + j);
                    if(*(ptn + j) > *(ptf + j)) {
                        *(ptn + j) = 0;
                        *(pts + j) = *(pts + j) * 9 / 10;
                    }
                    (*(ptn + j))++;
                }
            }
            else {
                for(int j = 0; j < _num_neurons; j++) {
                    *(_ncurrent + j) += *(pts + j);
                    if(*(ptn + j) > *(ptf + j)) {
                        *(ptn + j) = 0;
                        *(pts + j) = *(pts + j) * 9 / 10;
                    }
                    (*(ptn + j))++;
                }
            }
        }
    }

    /* solving DE, reset post-syn current */
    for(int i = 0; i < _num_neurons; i++) {
        (_neurons + i)->iq(*(_ncurrent + i) + *(_biascurrent + i));
        *(_ncurrent + i) = 0;
    }

    return;
}

void iq_network::printfile(FILE **fp)
{
    int i;

    for(i = 0; i < _num_neurons; i++) {
        fprintf(fp[i], "%d\n", (_neurons+i)->potential());
    }
    return;
}

void iq_network::set_biascurrent(int neuron_index, int biascurrent)
{
    *(_biascurrent + neuron_index) = biascurrent;
    return;
}

int iq_network::potential(int neuron_index)
{
    return (_neurons + neuron_index)->potential();
}

int iq_network::spike_count(int neuron_index)
{
    return (_neurons + neuron_index)->spike_count();
}

float iq_network::spike_rate(int neuron_index)
{
    return (_neurons + neuron_index)->spike_rate();
}

void iq_network::set_num_threads(int num_threads)
{
    _num_threads = num_threads;
    omp_set_num_threads(num_threads);
    return;
}

extern "C"
{
    DLLEXPORTIQ iq_network* iq_network_new() {return new iq_network();}
    DLLEXPORTIQ int iq_network_num_neurons(iq_network* network) {return network->num_neurons();}
    DLLEXPORTIQ void iq_network_send_synapse(iq_network* network) {return network->send_synapse();}
    DLLEXPORTIQ void iq_network_set_biascurrent(iq_network* network, int neuron_index, int biascurrent) {return network->set_biascurrent(neuron_index, biascurrent);}
    DLLEXPORTIQ int iq_network_potential(iq_network* network, int neuron_index) {return network->potential(neuron_index);}
    DLLEXPORTIQ int iq_network_spike_count(iq_network* network, int neuron_index) {return network->spike_count(neuron_index);}
    DLLEXPORTIQ float iq_network_spike_rate(iq_network* network, int neuron_index) {return network->spike_rate(neuron_index);}
    DLLEXPORTIQ void iq_network_set_num_threads(iq_network* network, int num_threads) {return network->set_num_threads(num_threads);}
}

