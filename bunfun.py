# like the good old ones from stata back in the day

import numpy as np
import pandas as pd

def isid(ds, var, only_based_on_non_miss=True):
    ### gotta figure out error message ###
    if only_based_on_non_miss == False:
        assert ds.shape[0] == ds.groupby(var).ngroups, 'SHIT AINT ISID'
    else:
        assert ds[ds[var].isna()==False].shape[0] == ds[ds[var].isna()==False].groupby(var).ngroups, 'SHIT AINT ISID'





def tab(var, incl_miss=True, sort_by='alp'):
    """ STATA'S TAB COMMAND """
    tot = len(var)
    dict_c = {}

    if type(var[0]) == str:
        miss_count = 0
        for i in var:
            if len(i) > 0:
                if i in dict_c:
                    dict_c[i] += 1
                else:
                    dict_c[i] = 1
            else:
                miss_count += 1
    else:
        miss_count = 0
        for i in var:
            if ~np.isnan(i):
                if i in dict_c:
                    dict_c[i] += 1
                else:
                    dict_c[i] = 1
            else:
                miss_count += 1

    if sort_by == 'alp':
        a = sorted(list(dict_c.keys()))
        if miss_count > 0:
            a.append('MISSING')
            dict_c['MISSING'] = miss_count
    elif sort_by == 'asc':
#     else:
        if miss_count > 0:
            dict_c['MISSING'] = miss_count
        b = sorted(dict_c.items(),key=lambda x: x[1])
        a = [i[0] for i in b]
    else:
        if miss_count > 0:
            dict_c['MISSING'] = miss_count
        b = sorted(dict_c.items(),key=lambda x: x[1], reverse=True)
        a = [i[0] for i in b]

    a.append('TOTAL')
    dict_c['TOTAL'] = tot

    mll = 0                  # as in Maximum Lenth for Label
    mlv = len("Freq")        # as in Maximum Lenth for Value
    mlp = len("Perc")        # as in Maximum Lenth for Percentage
    for key, value in dict_c.items():
        dict_c[key] = ["{:,}".format(value), "{:.2%}".format(value / tot)]

        mll = max(mll, len(str(key)))
        mlv = max(mlv, len(dict_c[key][0]))
        mlp = max(mlp, len(dict_c[key][1]))

    print(" "*mll + "   " + "Freq"+ " "*(mlv-4) + "   " + "Perc"+ " "*(mlp-4) + "   Cum. Perc")
    cp = 0
    for i in a:
        for key, val in dict_c.items():
            if i == key:
                if i == 'TOTAL':
                    cp_out = ''
                else:
                    cp = cp + float(val[0].replace(',',''))
                    cp_out = "{:.2%}".format(cp / tot)

                print(str(key) + " "*(mll-len(str(key))) + "   " + str(val[0]) + " "*(mlv-len(str(val[0]))) + "   " + str(val[1]) + \
                      " "*(mlp-len(str(val[1]))) + "   " + cp_out  )
            else:
                continue
