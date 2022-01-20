import pandas as pd
import numpy as np
from services.utils import *

# def calculate_derived_features(df):
def cov_calc(master_df,prefix,no_of_months):
    for variable in ['COV_DBC']:  # COV_CR_DR_R, COV_CC, COV_CW, COV_MIN_BAL ,'COV_CD', 'COV_CRC', 'COV_CB', 'COV_AVG_BAL','COV_CC','COV_CR_DR_R','COV_MIN_BAL','COV_MAX_BAL'
        if variable == 'COV_CD':
            monthly_vars = month_vars_name('Debits', prefix)
        elif variable == 'COV_DBC':
            monthly_vars = month_vars_name('Debit Counts',prefix)
        elif variable == 'COV_CRC':
            monthly_vars = month_vars_name('Credit Counts',prefix)
        elif variable == 'COV_CB':
            monthly_vars = month_vars_name('Closing Balance',prefix)
        elif variable == 'COV_AVG_BAL':
            monthly_vars = month_vars_name('Average Balance',prefix)
        elif variable == 'COV_CC':
            monthly_vars = month_vars_name('Credits',prefix)
        elif variable == 'COV_CR_DR_R':
            monthly_vars = month_vars_name('CrDrR',prefix)
        elif variable == 'COV_MIN_BAL':
            monthly_vars = month_vars_name('Minimum Balance',prefix)
        elif variable == 'COV_MAX_BAL':
            monthly_vars = month_vars_name('Maximum Balance',prefix)

        for index, row in master_df.iterrows():
            value_list = []
            for col in monthly_vars[0:6]:
                # if col == 'B0M04 CrDrR':
                #     print(col)
                value_list.append(row[col])
            master_df.loc[index, prefix+"_"+variable] = cov(no_of_months, value_list)
    return master_df


def get_timely_variables(master_df,prefix):
    master_df[prefix+'_3mavgRev'] = master_df[[prefix+'M00 Credits',prefix+'M01 Credits',prefix+'M02 Credits']].mean(axis=1)
    master_df[prefix + '_6mavgRev'] = master_df[[prefix+'M00 Credits',prefix+'M01 Credits',prefix+'M02 Credits',prefix+'M03 Credits',prefix+'M04 Credits',prefix+'M05 Credits']].mean(axis=1)
    master_df[prefix + '_3mtotalRev'] = master_df[[prefix+'M00 Credits',prefix+'M01 Credits',prefix+'M02 Credits']].sum(axis=1)
    master_df[prefix + '_6mtotalRev'] = master_df[[prefix+'M00 Credits',prefix+'M01 Credits',prefix+'M02 Credits',prefix+'M03 Credits',prefix+'M04 Credits',prefix+'M05 Credits']].sum(axis=1)
    master_df[prefix + '_3mavgBalance'] = master_df[[prefix + 'M00 Average Balance', prefix + 'M01 Average Balance', prefix + 'M02 Average Balance']].mean(axis=1)
    master_df[prefix + '_6mavgBalance'] = master_df[[prefix + 'M00 Average Balance', prefix + 'M01 Average Balance', prefix + 'M02 Average Balance',prefix + 'M03 Average Balance',prefix + 'M04 Average Balance',prefix + 'M05 Average Balance']].mean(axis=1)

    master_df[prefix + '_6mavgCrCnt'] = master_df[[prefix + 'M00 Credit Counts', prefix + 'M01 Credit Counts', prefix + 'M02 Credit Counts', prefix + 'M03 Credit Counts',prefix + 'M04 Credit Counts', prefix + 'M05 Credit Counts']].mean(axis=1)
    master_df[prefix + '_3mavgCrCnt'] = master_df[[prefix + 'M00 Credit Counts', prefix + 'M01 Credit Counts', prefix + 'M02 Credit Counts']].mean(axis=1)

    return master_df

def get_growth_variables(master_df,prefix):
    master_df[prefix+"_rev_growth3m"] = np.where(master_df[prefix+'M02 Credits'] == 0, np.nan, ((master_df[prefix+'M00 Credits'] / master_df[prefix+'M02 Credits']) - 1))
    master_df[prefix + "_rev_growth6m"] = np.where(master_df[prefix+'M05 Credits'] == 0, np.nan, ((master_df[prefix+'M00 Credits'] / master_df[prefix+'M05 Credits']) - 1))

    return master_df