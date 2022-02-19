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
def tab(series):
  colname = 0 if series.name == None else series.name

  df = pd.DataFrame(series)
  tabulated = df.groupby(colname)[[colname]].count().rename(columns={colname:'cnt'})
  tabulated = tabulated[tabulated['cnt']>0]
  tabulated['perc'] = tabulated['cnt'] / len(df)

  if tabulated.index.dtype.name == 'category':
    tabulated.index = tabulated.index.astype(str)
#   elif tabulated.index.is_numeric() == True:
#     if tabulated.index.dtype.name in([np.int32, np.int16, np.int64]):
#       tabulated.index = tabulated.index.astype(float)
#     assign_value = np.nan
#   else:
#     assign_value = "rest"

  remaining = df[df[colname].isna()==True]
  if len(remaining) > 0:
    rest = (
      pd.DataFrame.from_dict(
        {
          colname: ["MISSING"],
          'cnt':   [len(remaining)],
          'perc':  [len(remaining)/len(df)]
        }
      ).set_index(colname)
    )

    tabulated = tabulated.append(rest)

  tabulated['cum_perc'] = tabulated['perc'].cumsum()
  tabulated['cum_perc'] = tabulated.apply(lambda x: "{:.2%}".format(x['cum_perc']), axis=1)

  total_row = (
    pd.DataFrame.from_dict(
      {
        colname: ["TOTAL"],
        'cnt': [tabulated['cnt'].sum()],
        'perc':  [1],
        'cum_perc': ""
      }
    ).set_index(colname)
  )
  tabulated = tabulated.append(total_row)
  tabulated['cnt'] = tabulated.apply(lambda x: "{:,}".format(x['cnt']), axis=1)
  tabulated['perc'] = tabulated.apply(lambda x: "{:.2%}".format(x['perc']), axis=1)

  return tabulated




# THANK YOU EMIL
def isconst(dsr, byvar, voi, _inds=False):
    """
      Emil's isconstant command.
      Upgraded a lil bit.
      byvar and voi MUST BE LISTS (in square brackets).
      Returns dataset with _inds_* variable if _inds==True
    """

    n_obs_width = len(str(len(dsr)))
    n_d = n_obs_width + (n_obs_width//3) + 1

    max_len = max([len(i) for i in voi]) + 2
    not_constant_indi = 0
    ds = dsr.copy()
    for v in voi:
        gbv = byvar + [v]
        gb = ds[gbv].copy().groupby(byvar).nunique()

        n_problem_byvar = len(gb[gb[v]>1])
        n_inconsist_obs = gb.loc[gb[v]>1,v].sum()

        if gb[v].max() > 1:
            not_constant_indi = 1
            print(
                "{:<{max_len}} NOT constant: {:<{n_d},.0f} byvars w/ {:<{n_d},.0f} values"\
                    .format(v, n_problem_byvar, n_inconsist_obs, max_len=max_len, n_d=n_d)
            )
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





def compare_dates(fm, tu, wr2='seconds', pv=.25, labs=['first date','second date'],
                   _ind = False
                  ):
    """
    compares 2 pandas timestamps in series
    """

    perc = np.arange(0,1,pv)


    print("*"*88)
    print("-"*55)
    if any(fm.isna()==True) | any(fm.isna()==True):
        print('{:<30} {:<12,.0f} {:<12,.2%}'\
              .format(f"Missing {labs[0]} only:",
                      sum((fm.isna()==True)&(tu.isna())==False),
                      sum((fm.isna()==True)&(tu.isna()==False))/len(fm))
        )
        print('{:<30} {:<12,.0f} {:<12,.2%}'\
              .format(f"Missing {labs[1]} only:",
                      sum((fm.isna()==False)&(tu.isna())==True),
                      sum((fm.isna()==False)&(tu.isna()==True))/len(fm))
        )
        print('{:<30} {:<12,.0f} {:<12,.2%}'\
              .format('Both not missing:',
                      sum((fm.isna()==False)&(tu.isna())==False),
                      sum((fm.isna()==False)&(tu.isna()==False))/len(fm))
        )
        _n = sum((fm.isna()==False)&(tu.isna()==False))
    else:
        print('Nothing missing in both dates')
        _n = len(fm)

    print("-"*55)
#     diff = (tu - fm).dt.seconds
    comps = (tu - fm).dt.components
    diff = convert_td_components_to_values(comps, wr2)
    same = diff == 0
    d1_b = diff <  0
    d2_b = diff >  0
    print(
      '{:<30} {:<12,.0f} {:<12,.2%}'.format('Same:',sum(diff==0), sum(same)/_n)
    )
    print(
      '{:<30} {:<12,.0f} {:<12,.2%}'.format(f"{labs[0]} earlier:",sum(diff>0), sum(diff>0)/_n)
    )
    print(
      '{:<30} {:<12,.0f} {:<12,.2%}'.format(f"{labs[1]} earlier:",sum(diff<0), sum(diff<0)/_n)
    )
    print("-"*55)

    c = pd.concat([diff[d2_b].describe(percentiles=perc),
                   diff[d1_b].describe(percentiles=perc)], axis=1)
    c.columns = [f"{labs[0]} earlier by:", f"{labs[1]} earlier by:"]

    print(c.to_string(formatters={f"{labs[0]} earlier by:":"{:.2f}".format,
                                  f"{labs[1]} earlier by:":"{:.2f}".format}))

    if _ind == True:
        return np.where(diff==0, 'same',\
               np.where(diff> 0, f"{labs[0]} earlier",f"{labs[1]} earlier"))

    print("-"*55)
    print("*"*88)





def order(ds, voi, front=True):
    """ STATA'S DATASET ORDERING COMMAND """
    cols = list(ds.columns)
    for v in voi:
        cols.remove(v)

    c2u = voi + cols if front == True else cols + voi
    return ds[c2u]





def count_missing(ds):
    """ emil's count_missing command """
    if ds.isna().any().any():
        print(
            (ds.isna().sum()[ds.isna().sum()>0] / len(ds)).apply("{:.2%}".format)
        )
    else:
        print('AINT NUTHIN BUT A GANGSTA PAR-TY')
