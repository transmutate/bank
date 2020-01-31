import numpy as np
import pandas as pdb
import matplotlib.pyplot as plt
import seaborn as sns
sns.set(context='paper', style='darkgrid', rc={'figure.facecolor':'white'}, font_scale=1.2)





def daily_line_plot(ds,voi):
    f, ax = plt.subplots(figsize=(30,30))
    plt.subplot(3, 1, 1)
    plt.title('ALL DAYS')
    plt.plot(ds[voi])
    plt.ylim(bottom=0)

    plt.subplot(3, 1, 2)
    plt.title('EXCEPT SUNDAYS')
    plt.plot(ds.loc[ds['dow']!='Sunday',voi])
    plt.ylim(bottom=0)

    plt.subplot(3, 1, 3)
    plt.title('EXCEPT SUNDAYS & HOLIDAYS')
    plt.plot(ds.loc[(ds['dow']!='Sunday') & (ds['hday_indi']==0),voi])
    plt.ylim(bottom=0)





def yearly_monthly_level_plot(yoi, ds, v):
    daily = ds
    f, ax = plt.subplots(figsize=(30,18))
    c = 1
    r = 1
    title = ''
    hdays = daily['hday_indi']==1
    sunds = daily['dow']=='Sunday'
    ylim_dict = {
        'all':          [0, daily[v].max()],
        'excl_sun':     [0, daily.loc[(~sunds),v].max()],
        'excl_sun_hol': [0, daily.loc[(~sunds)&(~hdays),v].max()]
    }
    for run in ['all','excl_sun','excl_sun_hol']:
        for y in yoi:
            d = []
            lab = []
            tit = ''
            for m in range(1,13):
                if run=='all':
                    t = daily.loc[(daily['y']==y) & (daily['m']==m),v]
                elif run=='excl_sun':
                    t = daily.loc[(daily['y']==y) & (daily['m']==m) & (~sunds),v]
                else:
                    t = daily.loc[(daily['y']==y) & (daily['m']==m) & (~sunds) & (~hdays),v]
                lab.append(str(m))
                d.append(t)
            if run == 'all':
                tit = f'{str(y)}: ALL DAYS'
            elif run == 'excl_sun':
                tit = f'{str(y)}: EXCEPT SUNDAYS'
            else:
                tit = f'{str(y)}: EXCEPT SUNDAYS & HOLIDAYS'

            plt.subplot(3, 5, c)
            ax = sns.boxplot(data=d)
            ax.set_xticklabels(lab)
            ax.set_title(tit)
            ax.set_ylim([0,daily[v].max()])
            c = c + 1





def year_dow_level_plot(yoi, ds, voi, tit, rnum, st_pos):
    y2u = yoi
    daily = ds
    c = st_pos
    r = 1
    for v in [voi]:
        for y in y2u:
            d = []
            lab = []
            nobs = []
            meds = []
            for n in ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday','Holiday']:
                if n != 'Holiday':
                    t = daily.loc[(daily['y']==y) & (daily['hday_indi']==0) & (daily['dow']==n),v]
                else:
                    t = daily.loc[(daily['y']==y) & (daily['hday_indi']==1),v]
                d.append(t)
                nobs.append(str(t.shape[0]))
                meds.append(t.median())
                lab.append(n)

            plt.subplot(rnum, 5, c)
            ax = sns.boxplot(data=d)
            ax.set_xticklabels(lab)
            ax.set_title(f'{str(y)}: {tit}')
            ax.set_ylim([daily[v].min(),daily[v].max()])
            plt.xticks(rotation=45)

            pos = range(len(lab))
            for tick,label in zip(pos,ax.get_xticklabels()):
                ax.text(pos[tick], meds[tick] + 0.03, nobs[tick],
                horizontalalignment='center', size='medium', color='w', weight='semibold')

            c = c + 1





def year_dow_w_nohand_level_plot(yoi, ds, voi, tit):
    y2u = yoi
    f, ax = plt.subplots(figsize=(30,6))
    daily = ds
    c = 1
    r = 1
    weekdays = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']
    rest = ['Holiday Only','No Hand Only','At Least 2']

    for v in [voi]:
        for y in y2u:
            subs = daily[daily['y']==y]
            hday = subs['hday_indi']==1
            nohd = subs['no_hand_indi']==1
            sund = subs['sunday_indi']==1
            rest_dict = {
                'Holiday Only':      ( hday) & (~nohd) & (~sund) ,
                'No Hand Only':      (~hday) & ( nohd) & (~sund) ,
                'At Least 2':        (( hday)&( nohd)&(~sund)) | \
                                     (( hday)&(~nohd)&( sund)) | \
                                     ((~hday)&( nohd)&( sund)) | \
                                     (( hday)&( nohd)&( sund))
            }
            d = []
            lab = []
            nobs = []
            meds = []
            for n in weekdays + rest:
                if n in weekdays:
                    t = subs.loc[(subs['dow']==n) & (~hday) & (~nohd),v]
                else:
                    t = subs.loc[rest_dict[n],v]

                d.append(t)
                nobs.append(str(t.shape[0]))
                meds.append(t.median())
                lab.append(n)

            plt.subplot(1, 5, c)
            ax = sns.boxplot(data=d)
            ax.set_xticklabels(lab)
            ax.set_title(f'{str(y)}: {tit}')
            ax.set_ylim([daily[v].min(),daily[v].max()])
            plt.xticks(rotation=90)

            pos = range(len(lab))
            for tick,label in zip(pos,ax.get_xticklabels()):
                ax.text(pos[tick], meds[tick] + 0.03, nobs[tick],
                horizontalalignment='center', size='medium', color='w', weight='semibold')

            c = c + 1





def year_dow_level_for_no_hand_days_plot(yoi, ds, voi, tit, rnum, st_pos):
    y2u = yoi
    daily = ds
    c = st_pos
    r = 1
    dayz = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday','Holiday']
    for v in [voi]:
        for y in y2u:
            subs = daily[(daily['y']==y) & (daily['no_hand_indi']==1)]
            hday = subs['hday_indi']==1
            d = []
            lab = []
            nobs = []
            meds = []
            for n in dayz:
                if n != 'Holiday':
                    t = subs.loc[(subs['dow']==n) & (~hday),v]
                else:
                    t = subs.loc[(hday),v]

                d.append(t)
                nobs.append(str(t.shape[0]))
                meds.append(t.median())
                lab.append(n)

            plt.subplot(rnum, 5, c)
            ax = sns.boxplot(data=d)
            ax.set_xticklabels(lab)
            ax.set_title(f'{str(y)}: {tit}')
            ax.set_ylim([daily[v].min(),daily[v].max()])

            plt.xticks(rotation=90)

            pos = range(len(lab))
            for tick,label in zip(pos,ax.get_xticklabels()):
                ax.text(pos[tick], meds[tick] + 0.03, nobs[tick],
                horizontalalignment='center', size='medium', color='w', weight='semibold')

            c = c + 1
