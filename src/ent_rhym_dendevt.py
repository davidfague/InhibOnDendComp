"""Measure entrainment of dendritic events by rhythmic signal
Author: Drew B. Headley

"""
import numpy as np
from .bin_serser import bin_serser
from .ppc import ppc2
def ent_rhym_dendevt(seg_df, rhym_ser):
    """
    For each segment's dendritic event time series measure it entrainment
    with PPC to a rhythmic series.

    Parameters
    ----------
    seg_df : dataframe
        dendritic spike events series by segment
    rhym_ser : numpy array
        the rhythmic signal to be binned with

    Returns
    ----------
    bin_df : dataframe
        binned for each dendritic event. Column name is 'ph_bin'

    Examples
    ----------

    """

    # set bin edges
    if edges is None:
        edges = np.linspace(-np.pi, np.pi, bin_num)
    

    # determine event names
    ser_colname = [x for x in seg_df.columns if x.endswith("_ser")][0]

    # get spike triggered average, expressed as percent change from mean
    prc_func = lambda bin, m: ((bin - m) / m) * 100
    ppc_temp = []
    for _, x in seg_df.iterrows():
        ppc_temp.append(ppc2(rhym_ser[np.where(np.diff(x[ser_colname].flatten()) > 0)[0] + 1]))
    seg_df["ppc"] = ppc_temp

    # merge segments by electronic distance quantile
    agg_func = {"ppc": lambda x: np.vstack(x)}
    bin_df = seg_df.groupby(["Elec_distanceQ", "Type"]).aggregate(agg_func)

    # mean percent change and t-stats by electrotonic distance
    bin_m = []
    for _, x in bin_df.iterrows():
        bin_m.append(np.nanmedian(x["ppc"], 0))

    bin_df["ppc"] = bin_m

    return bin_df


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
