"""Bin dendritic events phases and calculate entrainment with PPC.
Author: Drew B. Headley

"""
import numpy as np
from .ppc import ppc2
from .bin_serser import bin_serser


def ph_rhym_dendevt(seg_df, bin_num, edges=None):
    """
    For each segment's dendritic event time series it is binned with
    respect to a rhythmic series.

    Parameters
    ----------
    seg_df : dataframe
        dendritic spike events series by segment
    bin_num : integer
        number of bins to use for the rhym_ser
    edges : array-like
        bin edges, overrides bin_num

    Returns
    ----------
    hist_df : dataframe
        binned histogram of dendritic events by phase, expressed as percent change from mean
    ppc_df : dataframe
        entrainment of dendritic events to phase, expressed as PPC

    Examples
    ----------

    """

    # set bin edges
    if edges is None:
        edges = np.linspace(-np.pi, np.pi, bin_num)
    

    # determine event names
    ph_colnames = [x for x in seg_df.columns if x.endswith("_ph")]

    # get spike triggered average, expressed as percent change from mean
    prc_func = lambda x: ((x - np.mean(x)) / np.mean(x)) * 100

    for ph_colname in ph_colnames:
        seg_df[ph_colname + "_hist"] = seg_df.apply(
            lambda x: prc_func(np.histogram(
                x[ph_colname].astype(float),
                bins=edges)[0]),
                axis=1
        )
        
        seg_df[ph_colname + "_ppc"] = seg_df.apply(
            lambda x: ppc2(x[ph_colname]), 
            axis=1
        )
        
    # merge segments by electronic distance quantile
    agg_func = lambda x: np.nanmedian(np.stack(x,axis=0), axis=0)
    hist_df = seg_df.groupby(["Elec_distanceQ", "Type"])[[x +'_hist' for x in ph_colnames]].aggregate(agg_func)

    ppc_df = seg_df.groupby(["Elec_distanceQ", "Type"])[[x + '_ppc' for x in ph_colnames]].aggregate(agg_func)

    return hist_df, ppc_df


if __name__ == "__main__":
    """from load_spike_h5 import load_spike_h5
    from load_dendevt_csv import load_dendevt_csv
    from seg_dendevt import seg_dendevt
    from ser_seg_dendevt import ser_seg_dendevt

    print("Testing calcium spikes with sta_ap_dendevt.py")
    ca_fpath_test = (
        "Y:\\DendCompOsc\\16Hzapical_exc_mod\\"
        "output_16Hz_dend_inh_0deg_exc_10p_ca.csv"
    )
    ap_fpath_test = (
        "Y:\\DendCompOsc\\16Hzapical_exc_mod\\"
        "output_16Hz_dend_inh_0deg_exc_10p\\spikes.h5"
    )

    dspk_test = load_dendevt_csv(ca_fpath_test)
    ap_test = load_spike_h5(ap_fpath_test)
    seg_test = seg_dendevt(dspk_test)
    seg_test = ser_seg_dendevt(seg_test, step_len=20, win_lim=[0, 2000000])
    sta_test = sta_ap_dendevt(seg_test, np.round(ap_test / 20), bin=1, win=[-100, 100])
    print(sta_test)"""
