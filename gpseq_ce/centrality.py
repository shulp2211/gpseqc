# -*- coding: utf-8 -*-

'''
@author: Gabriele Girelli
@contact: gigi.ga90@gmail.com
@description: centrality estimation methods.
'''

# DEPENDENCIES =================================================================

import numpy as np
import pandas as pd
from tqdm import tqdm

# FUNCTIONS ====================================================================

def calc_p(st, ci):
    '''Calculate restriction probability.

    Args:
        st (pd.DataFrame): bin-based data frame (over conditions).
        ci (int): condition index.

    Returns:
        float
    '''
    assert ci < st.shape[0], "requested condition (index) not found."
    row = st.iloc[ci, :]
    return(row['sum'] / (row['cond_nreads'] * row['count']))

def calc_pc(st, ci):
    '''Calculate cumulative restriction probability.

    Args:
        st (pd.DataFrame): bin-based data frame (over conditions).
        ci (int): condition index.

    Returns:
        float
    '''
    assert ci < st.shape[0], "requested condition (index) not found."
    if ci == 0: return(calc_p(st, 0))
    else: return(calc_p(st, ci) + calc_pc(st, ci - 1))

def calc_pr(st, ci):
    '''Calculate probability of cumulative restriction.

    Args:
        st (pd.DataFrame): bin-based data frame (over conditions).
        ci (int): condition index.

    Returns:
        float
    '''
    assert ci < st.shape[0], "requested condition (index) not found."
    if ci == 0: return(calc_p(st, 0))
    else:
        p = st.ix[:ci, "sum"].sum()
        p /= np.sum(st.ix[:ci, "cond_nreads"].values * st.ix[:ci, "count"].values)
        return(p)

def calc_var(st, ci):
    '''Calculate variance.

    Args:
        st (pd.DataFrame): bin-based data frame (over conditions).
        ci (int): condition index.

    Returns:
        np.float64
    '''
    assert ci < st.shape[0], "requested condition (index) not found."
    return(np.power(st.ix[ci, "std"], 2))

def calc_ff(st, ci):
    '''Calculate Fano Factor.

    Args:
        st (pd.DataFrame): bin-based data frame (over conditions).
        ci (int): condition index.

    Returns:
        np.float64
    '''
    assert ci < st.shape[0], "requested condition (index) not found."
    return(np.power(st.ix[ci, "std"], 2) / st.ix[ci, "mean"])

def calc_cv(st, ci):
    '''Calculate coefficient of variation

    Args:
        st (pd.DataFrame): bin-based data frame (over conditions).
        ci (int): condition index.

    Returns:
        np.float64
    '''
    assert ci < st.shape[0], "requested condition (index) not found."
    return(st.ix[ci, "std"] / st.ix[ci, "mean"])

def est_2p(st, f1, f2):
    '''Estimates centrality by combining conditions with two-points fashion.

    Args:
        st (pd.DataFrame): bin-based data frame (over conditions).
        f1 (fun): function for calculating condition-wise metrics.
        f2 (fun): function for putting conditions together.

    Returns:
        Estimated centrality.
    '''
    a = f1(st, 0)
    b = f1(st, st.shape[0] - 1)
    return(f2(b, a))

def est_f(st, f1, f2):
    '''Estimates centrality by combining conditions with fixed fashion.

    Args:
        st (pd.DataFrame): bin-based data frame (over conditions).
        f1 (fun): function for calculating condition-wise metrics.
        f2 (fun): function for putting conditions together.

    Returns:
        Estimated centrality.
    '''
    out = 0
    a = f1(st, 0)
    for i in range(1, st.shape[0]):
        b = f1(st, i)
        out += f2(b, a)
    return(out)

def est_g(st, f1, f2):
    '''Estimates centrality by combining conditions with global fashion.

    Args:
        st (pd.DataFrame): bin-based data frame (over conditions).
        f1 (fun): function for calculating condition-wise metrics.
        f2 (fun): function for putting conditions together.

    Returns:
        Estimated centrality.
    '''
    out = 0
    a = f1(st, 0)
    for i in range(1, st.shape[0]):
        b = f1(st, i)
        out += f2(b, a)
        a = b
    return(out)

def bin_estimate(df, mlist, progress = True):
    '''Estimate centrality for each bin in a condition combined data frame.

    Args:
        df (pd.DataFrame): multi-condition data frame.
        mlist (list): list of metrics to calculate.
        progress (bool): show progress bar.
    '''

    # Build generator
    indexes = list(set(df.index))
    igen = (i for i in indexes)
    if progress: igen = tqdm(igen, total = len(indexes))

    # Iterate over bins
    odf = []
    for i in igen:
        st = df.loc[i, :]
        st.index = range(st.shape[0])

        # Prepare output
        orow = st.ix[0, ['chrom', 'start', 'end']]

        # Calculate requested metrics
        for m in mlist:
            # Probability
            if m == "prob_2p": # two-points
                orow[m] = est_2p(st, calc_p, lambda x, y: x / y)
            elif m == "prob_f": # fixed
                orow[m] = est_f(st, calc_p, lambda x, y: x / y)
            elif m == "prob_g": # global
                orow[m] = est_g(st, calc_p, lambda x, y: x / y)

            # Cumulative ratio
            elif m == "cor_2p": # two-points
                orow[m] = est_2p(st, calc_pc, lambda x, y: x / y)
            elif m == "cor_f": # fixed
                orow[m] = est_f(st, calc_pc, lambda x, y: x / y)
            elif m == "cor_g": # global
                orow[m] = est_g(st, calc_pc, lambda x, y: x / y)

            # Ratio of cumulative
            elif m == "roc_2p": # two-points
                orow[m] = est_2p(st, calc_pr, lambda x, y: x / y)
            elif m == "roc_f": # fixed
                orow[m] = est_f(st, calc_pr, lambda x, y: x / y)
            elif m == "roc_g": # global
                orow[m] = est_g(st, calc_pr, lambda x, y: x / y)

            # Variance
            elif m == "var_2p": # two-points
                orow[m] = est_2p(st, calc_var, lambda x, y: np.log(x / y))
            elif m == "var_f": # fixed
                orow[m] = est_f(st, calc_var, lambda x, y: np.log(x / y))

            # Fano factor
            elif m == "ff_2p": # two-points
                orow[m] = est_2p(st, calc_ff, lambda x, y: y - x)
            elif m == "ff_f": # fixed
                orow[m] = est_f(st, calc_ff, lambda x, y: y - x)

            # Coefficient of variation
            elif m == "cv_2p": # two-points
                orow[m] = est_2p(st, calc_cv, lambda x, y: y - x)
            elif m == "cv_f": # fixed
                orow[m] = est_f(st, calc_cv, lambda x, y: y - x)

        odf.append(orow)

    # Assemble output
    odf = pd.concat(odf, axis = 1).transpose()
    columns = ['chrom', 'start', 'end']
    columns.extend(mlist)
    odf.columns = columns[:odf.shape[1]]
    odf.index = range(odf.shape[0])

    return(odf)

def rank(cdf, mlist, progress = True, chrWide = False):
    ''''''
    if chrWide:
        labels = [cdf["chrom"].values[i] for i in cdf.index]
    else:
        labels = ["%s:%s-%s" % tuple(cdf.ix[i, :].tolist()[:3])
            for i in cdf.index]
    
    gen = (m for m in mlist if m in cdf.columns)
    if progress: gen = tqdm(gen, total = len(mlist))

    odf = []
    for m in gen:
        odf.append([labels[i] for i in np.argsort(cdf[m].values)])
    
    odf = pd.DataFrame(odf).transpose()
    odf.columns = [m for m in mlist if m in cdf.columns]

    return(odf)

# END ==========================================================================

################################################################################
