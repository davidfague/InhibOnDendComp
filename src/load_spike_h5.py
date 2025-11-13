""" Creates numpy array from an H5 file containing somatic spike events
Author: Drew B. Headley

"""


import numpy as np
import h5py


def load_spike_h5(fpath):
    """
    Loads an H5 file that contains somatic action potential times and the
    converts them to a numpy array of integer simulation time steps

    Parameters
    ----------
    fpath : string
        full file path to the H5 file

    Returns
    ----------
    spk_t : numpy array of integers
        simulation time steps where an action potential was emitted at
        the soma

    Examples
    ----------

    """
    try: # original loading
        spikes = h5py.File(fpath, "r")
        spk_t = np.array(spikes["spikes"]["biophysical"]["timestamps"])

        # Convert spike times to integers and sort
        # assumes times are in ms and simulation had dt = 0.1 ms (10 kHz sampling rate)
        spk_t = np.sort(np.round(spk_t * 10).astype(int))

        return spk_t
    except: # load from pipeline (other users would need to update the path)
        import sys
        sys.path.append("/home/drfrbc/Neural-Modeling/")
        from Modules import analysis
        spk_t = np.sort((analysis.DataReader.read_data(fpath, "soma_spikes")[0][:] * 10).astype(int))
        return spk_t



if __name__ == "__main__":
    print("Testing load_spike_h5.py")
    fpath_test = "../Data/spikes.h5"
    spk_test = load_spike_h5(fpath_test)
    print(spk_test)
