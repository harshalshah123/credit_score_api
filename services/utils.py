import pandas as pd
import numpy as np
import re
from scipy import interpolate
import datetime
from dateutil.relativedelta import relativedelta


def month_vars_name(var,prefix, sep=' '):
    var_list = [(prefix +'M' + '0' + str(i) + sep + var) if i < 10 else (prefix + 'M' + str(i) + sep + var) for i in range(12)]
    return var_list



def pivot_bal(data, col, val, suffix,indexcol, nan_zero_flag=False):
    data1 = data.copy()
    data1 = data1.pivot(index=indexcol, columns=col, values=val)
    # data1.drop(['nan'], inplace = True, axis = 1)
    if nan_zero_flag:
        data1.replace(np.nan, 0, inplace=True)
    data1.columns = [str(column) + suffix for column in data1.columns]
    data1 = data1.reset_index()
    return data1

def pivot_processing(df,indexcol):

    cnt = 0
    for col in df.columns.values:
        if (col != indexcol) and (col != 'mno'):
            pivot = pivot_bal(data=df, col='mno', val=col, suffix=' ' + str(col),indexcol=indexcol, nan_zero_flag=True)
            if cnt == 0:
                master_pivot = pivot.copy()
            else:
                master_pivot = pd.merge(master_pivot, pivot, how='left', on=indexcol)
            cnt += 1

    return master_pivot


def divide(x, y):
    if y == 0:
        return 0
    else:
        return (float(x / y))


def cov(n, value_list):
    # print(n)
    scs = value_list[0:n]
    cov = divide(np.std(scs, ddof=1), np.mean(scs)) * 100
    # print cov
    return cov

def string_found(string1, string2):
   if re.search(r"\b" + re.escape(string1) + r"\b", string2):
      return True
   return False

def extractSignal_kalmanFiltering(observations):
  '''

  :param observations:
  :return:
  '''
  try:
    # intial parameters
    z = np.array(observations)
    n_iter = len(z)
    sz = (n_iter,)  # size of array

    Q = 1e-5  # process variance

    # allocate space for arrays
    xhat = np.zeros(sz)  # a posteri estimate of x
    P = np.zeros(sz)  # a posteri error estimate
    xhatminus = np.zeros(sz)  # a priori estimate of x
    Pminus = np.zeros(sz)  # a priori error estimate
    K = np.zeros(sz)  # gain or blending factor

    R = 0.1 ** 2  # estimate of measurement variance, change to see effect

    # intial guesses
    xhat[0] = 0.0
    P[0] = 1.0

    for k in range(1, n_iter):
      # time update
      xhatminus[k] = xhat[k - 1]
      Pminus[k] = P[k - 1] + Q

      # measurement update
      K[k] = Pminus[k] / (Pminus[k] + R)
      xhat[k] = xhatminus[k] + K[k] * (z[k] - xhatminus[k])
      P[k] = (1 - K[k]) * Pminus[k]

    return xhat
  except Exception as ex:
    raise ex

def extrapolate(observations, n):
  '''
  Extrapolate income signal linearly
  :param observations:
  :param n:
  :return:
  '''

  try:
    s = interpolate.interp1d(np.array(range(len(observations))), observations, fill_value='extrapolate')
    intep1d_val = [np.round(s(i), 2) for i in range(len(observations), len(observations) + n)]

    return intep1d_val
  except Exception as ex:
    raise ex

def get_month_day_range(date):

    last_day = date + relativedelta(day=1, months=+1, days=-1)
    first_day = date + relativedelta(day=1)
    return first_day, last_day

def woe_transformation(X, woe_bins, reverse_flag=False):
    vars_miss_flag = woe_bins.groupby(['var']).agg({'miss_flag': np.sum}).reset_index()
    obj_cols = woe_bins[['var']][woe_bins['dtype'] == 'object'].drop_duplicates()
    obj_cols = pd.merge(obj_cols, vars_miss_flag, on='var')
    woe_data = pd.DataFrame(index=X.index)
    for col in obj_cols['var']:
        # print col
        if obj_cols['miss_flag'][(obj_cols['var'] == col)].any() == 1:
            miss_woe = woe_bins['woe'][(woe_bins['miss_flag'] == 1) & (woe_bins['var'] == col)].iloc[0]
            var_miss_data = X[col][pd.isnull(X[col])]
            var_miss_data.replace(np.nan, miss_woe, inplace=True)
        non_miss_woe = woe_bins[['woe', 'bin']][(woe_bins['miss_flag'] == 0) & (woe_bins['var'] == col)]
        var_nmiss_data = X[col][~pd.isnull(X[col])]
        non_miss_woe = non_miss_woe.set_index('bin')
        non_miss_woe = non_miss_woe.T.squeeze()
        var_nmiss_data = var_nmiss_data.map(non_miss_woe)
        if obj_cols['miss_flag'][(obj_cols['var'] == col)].any() == 1:
            var_woe = var_miss_data.append(var_nmiss_data)
        else:
            var_woe = var_nmiss_data.copy()
        var_woe.sort_index(inplace=True)
        woe_data = woe_data.join(var_woe)

    num_cols = woe_bins[['var']][woe_bins['dtype'] != 'object'].drop_duplicates()
    num_cols = pd.merge(num_cols, vars_miss_flag, on='var')
    for col in num_cols['var']:
        # print col
        # if col == LOAN_INQUIRY:
        #      print("woo")
        if num_cols['miss_flag'][(num_cols['var'] == col)].any() == 1:
            miss_woe = woe_bins['woe'][(woe_bins['miss_flag'] == 1) & (woe_bins['var'] == col)].iloc[0]
            var_miss_data = X[col][pd.isnull(X[col])]
            var_miss_data.replace(np.nan, miss_woe, inplace=True)
        non_miss_woe = woe_bins[['woe', 'bin']][(woe_bins['miss_flag'] == 0) & (woe_bins['var'] == col)]
        var_nmiss_data = X[col][~pd.isnull(X[col])]
        non_miss_woe = non_miss_woe[['woe']].reset_index(drop=True)
        non_miss_woe['bin'] = non_miss_woe.index
        non_miss_woe = non_miss_woe.set_index('bin')
        non_miss_woe = non_miss_woe.iloc[:, 0]
        bin_cuts = woe_bins['bin_cuts'][woe_bins['var'] == col].dropna()
        # bin_cuts = np.append(bin_cuts,(var_nmiss_data.max() + 1))
        if reverse_flag:
            if float(bin_cuts.min()) < float(var_nmiss_data.min()):
                bin_cuts = np.append((bin_cuts.min() - 1), bin_cuts)
            else:
                bin_cuts = np.append(var_nmiss_data.min() - 1, bin_cuts)
            if bin_cuts.max() < var_nmiss_data.max():
                bin_cuts[len(bin_cuts) - 1] = var_nmiss_data.max()
        else:
            if float(bin_cuts.max()) < float(var_nmiss_data.max()):
                bin_cuts = np.append(bin_cuts, (var_nmiss_data.max() + 1))
            else:
                bin_cuts = np.append(bin_cuts, (bin_cuts.max() + 1))

            if bin_cuts.min() > var_nmiss_data.min():
                bin_cuts[len(bin_cuts) - 1] = var_nmiss_data.min()

        bins = pd.cut(var_nmiss_data, bin_cuts, labels=non_miss_woe.index)
        var_nmiss_data = bins.map(non_miss_woe)
        if num_cols['miss_flag'][(num_cols['var'] == col)].any() == 1:
            var_woe = var_miss_data.append(var_nmiss_data)
        else:
            var_woe = var_nmiss_data.copy()
        var_woe.sort_index(inplace=True)
        woe_data = woe_data.join(var_woe)
    return woe_data


def rename_dict_keys(mydict):
    mydict = {k.lower(): v for k, v in mydict.items()}
    mydict = {k.replace(' ','_'): v for k, v in mydict.items()}

    return mydict