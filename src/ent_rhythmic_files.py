""" Entrainment of dendritic events with respect to an ongoing rhythm
Author: Drew B. Headley

"""
import numpy as np
import pandas as pd
from .load_dendevt_csv import load_dendevt_csv
from .load_spike_h5 import load_spike_h5
from .seg_dendevt import seg_dendevt
from .ph_seg_dendevt import ph_seg_dendevt
from .ph_rhym_dendevt import ph_rhym_dendevt


def ent_rhythmic_files(dend_fname, rhym_ser, step, bin_num):
    """
    Uses the files for the dendritic events and phase of an afferent rhythm,
    calculate entrainment to a rhythm using PPC by a dendritic segment's 
    electrotonic distance.

    Parameters
    ----------
    dend_fname : string
        file path for dendritic spike events csv
    rhym_ser : numpy array
        starting phase of the rhythm
    step : int
        step size for the rhythmic signal, in samples
    bin_num : int
        number of bins to use for phase binning (from -pi to pi)

    Returns
    ----------
    dend_hist : dataframe
        binned histogram of dendritic events by phase, expressed as percent change from mean
    dend_ppc : dataframe
        entrainment of dendritic events to phase, expressed as PPC

    Examples
    ----------

    """
    dend_t = load_dendevt_csv(dend_fname)

    dend_seg = seg_dendevt(dend_t)
    dend_seg = ph_seg_dendevt(dend_seg, rhym_ser, step)
    dend_hist, dend_ppc = ph_rhym_dendevt(dend_seg, bin_num=bin_num)


    dend_hist = dend_hist.groupby(("Type")).aggregate(np.vstack)
    dend_ppc = dend_ppc.groupby(("Type")).aggregate(list).apply(np.array)
    return dend_hist, dend_ppc


if __name__ == "__main__":
    """
    print("Testing calcium spikes with sta_files.py")
    ca_fpath_test = (
        "Y:\\DendCompOsc\\16Hzapical_exc_mod\\"
        "output_16Hz_dend_inh_0deg_exc_10p_ca.csv"
    )
    ap_fpath_test = (
        "Y:\\DendCompOsc\\16Hzapical_exc_mod\\"
        "output_16Hz_dend_inh_0deg_exc_10p\\spikes.h5"
    )

    sta_test = sta_files(ca_fpath_test, ap_fpath_test, 20, [0, 2000000], 1, [-100, 100])
    print(sta_test)
    """
