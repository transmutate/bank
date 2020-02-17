# like the good old ones from stata back in the day

import numpy as np
import pandas as pd

def isid(ds, var, only_based_on_non_miss=True):
    ### gotta figure out error message ###
    if only_based_on_non_miss == False:
        assert ds.shape[0] == ds.groupby(var).ngroups, 'SHIT AINT ISID'
    else:
        assert ds[ds[var].isna()==False].shape[0] == ds[ds[var].isna()==False].groupby(var).ngroups, 'SHIT AINT ISID'





# like the good old ones from stata back in the day
def tab(var, incl_miss=True, sort_by='alp'):
    """ STATA'S TAB COMMAND """
    var = var.astype(str)
    tot = len(var)
    dict_c = {}

    miss_count = 0
    for i in var:
        if i != 'nan':
            if i in dict_c:
                dict_c[i] += 1
            else:
                dict_c[i] = 1
        else:
            miss_count += 1

    if sort_by == 'alp':
        t = pd.DataFrame.from_dict(dict_c, orient='index', columns=['count']).sort_index()
        t = t.append(pd.DataFrame({'count':miss_count}, index=['MISSING']))
    elif sort_by == 'des':
        t = pd.DataFrame.from_dict(dict_c, orient='index', columns=['count'])
        t = t.append(pd.DataFrame({'count':miss_count}, index=['MISSING']))
        t.sort_values('count',ascending=False, inplace=True)
    else:
        t = pd.DataFrame.from_dict(dict_c, orient='index', columns=['count'])
        t = t.append(pd.DataFrame({'count':miss_count}, index=['MISSING']))
        t.sort_values('count', inplace=True)

    t['perc'] = t['count'] / t['count'].sum()
    t['cum_perc'] = t['perc'].cumsum()

    t = t.append(pd.DataFrame({'count':[tot], 'perc':[1]}, index=['TOTAL']))

    t = t[['count','perc','cum_perc']]
    T = t.style.format({'count':'{:,}', 'perc':'{:.2%}', 'cum_perc':'{:.2%}'})
    display(T)
