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
        if miss_count > 0:
            t = t.append(pd.DataFrame({'count':miss_count}, index=['MISSING']))
    elif sort_by == 'des':
        t = pd.DataFrame.from_dict(dict_c, orient='index', columns=['count'])
        if miss_count > 0:
            t = t.append(pd.DataFrame({'count':miss_count}, index=['MISSING']))
        t.sort_values('count',ascending=False, inplace=True)
    else:
        t = pd.DataFrame.from_dict(dict_c, orient='index', columns=['count'])
        if miss_count > 0:
            t = t.append(pd.DataFrame({'count':miss_count}, index=['MISSING']))
        t.sort_values('count', inplace=True)

    t['perc'] = t['count'] / t['count'].sum()
    t['cum_perc'] = t['perc'].cumsum()

    t = t.append(pd.DataFrame({'count':[tot], 'perc':[1]}, index=['TOTAL']))

    t = t[['count','perc','cum_perc']]
    T = t.style.format({'count':'{:,}', 'perc':'{:.2%}', 'cum_perc':'{:.2%}'})
    return T




# THANK YOU EMIL
def isconst(dsr, byvar, voi, _inds=False):
  """ Emil's isconstant command. byvar and voi MUST BE LISTS (in square brackets). Returns dataset with _inds_* variable if _inds==True """
  not_constant_indi = 0
  # ds = dsr[byvar + voi].copy()
  ds = dsr.copy()
  for v in voi:
    gbv = byvar + [v]
    gb = ds[gbv].copy().groupby(byvar).nunique()
    if gb[v].max() > 1:
      not_constant_indi = 1
      print(f"Variable {v} is NOT constant by {byvar}")
      if _inds == True:
        gb = gb[[v]]
        gb.loc[:,v] = np.where(gb[v]==1, 0, gb[v])
        gb.rename(columns={v: f"_inds_{v}"}, inplace=True)
        gb.reset_index(inplace=True)
        ds = ds.merge(gb, on=byvar)

  if (_inds==True):
    if (not_constant_indi == 1):
      return ds
    else:
      return "EVERYTHANG CONSTANT"





def compare(ds, fir, sec):
    """ STATA'S COMPARE COMMAND """
    if ds[fir].dtype == object:
        boff = ds[[fir,sec]].dropna()
        firs = ds[fir].dropna()
        seco = ds[sec].dropna()

        print("_"*77)
        print(f"{fir} == {sec}: {len(boff[boff[fir]==boff[sec]]):,d}")
        print(f"{fir} != {sec}: {len(boff[boff[fir]!=boff[sec]]):,d}")
        print()
        print(f"jointly_defined: {' '*(max(len(fir),len(sec)))} {len(boff):,d}")
        print(f"{fir} missing only: {len(ds) - len(firs):,d}")
        print(f"{sec} missing only: {len(ds) - len(seco):,d}")
        print("-"*77)





def order(ds, voi, front=True):
    """ STATA'S DATASET ORDERING COMMAND """
    cols = list(ds.columns)
    for v in voi:
        cols.remove(v)

    c2u = voi + cols if front == True else cols + voi
    return ds[c2u]



def count_missing(ds):
    """ emil's count_missing command """
    print(
        (ds.isna().sum()[ds.isna().sum()>0] / len(ds)).apply("{:.2%}".format)
    )
