""" Creates binary time series of dendritic event occurrences
Author: Drew B. Headley

"""
import numpy as np
import sys

sys.path.append(".")  # have to do this for relative imports to work consistently
from .ser_pt import ser_pt


def ph_seg_dendevt(seg_df, rhym_ser, step=10):
    """
    Takes a dendritic events dataframe grouped by segment and returns the 
    phases at which the events in seg_df occur.

    Parameters
    ----------
    seg_df : dataframe
        dendritic spike events grouped by segment
    rhym_ser : numpy array
        the phase of the rhythmic signal.
    step : int, optional
        step size for the rhythmic signal, in samples. By default, it is set to 10.

    Returns
    ----------
    seg_df : dataframe
        dendritic spike events returned with their corresponding phase values. 
        Column names are '<event_type>_lower_bound_ph' for and
        '<event_type>_ph_upper_bound_ph'.

    Examples
    ----------

    """

    # determine event names
    low_colname = [x for x in seg_df.columns if x.endswith("lower_bound")][0]
    

    # determine event type
    evt_type = low_colname.split("_")[0]

    # function to round indices to nearest step
    to_idx = lambda x: np.floor(np.array(x) / step).astype(int)

    # if NMDA or Ca spikes, create start/stop series
    if (evt_type == "nmda") or (evt_type == "ca"):
        up_colname = [x for x in seg_df.columns if x.endswith("upper_bound")][0]
        seg_df[[low_colname+'_ph', up_colname+'_ph']] = seg_df.apply(
            lambda x: (
                rhym_ser[to_idx(x[low_colname])], 
                rhym_ser[to_idx(x[up_colname])]),
                axis=1,
                result_type='expand'
            )
    else:
        seg_df[low_colname + '_ph'] = seg_df.apply(
            lambda x: rhym_ser[to_idx(x[low_colname])], 
            axis=1
        )

    return seg_df