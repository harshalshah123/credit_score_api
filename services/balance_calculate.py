import numpy as np
import pandas as pd
from services import data_validate as dv

class BALANCE():
    def __init__(self):
        pass
    def _get_balances(self,trans_df,min_line_date):
        trans_df['month_year'] = pd.to_datetime(trans_df['date']).dt.to_period('M')

        max_date = trans_df['date'].max()
        min_date = trans_df['date'].min()
        num_months = (max_date.year - min_date.year) * 12 + (max_date.month - min_date.month)
        validity = dv.check_transaction_timeperiod(num_months)

        if validity:
            agg_trans  = trans_df.groupby(['date']).agg({'amount':np.sum}).reset_index()
            agg_trans = agg_trans.sort_values(by='date',ascending=False).reset_index(drop=True)
            # available_bal = trans_df['available'][0]
            available_bal = trans_df['current'][0]

            agg_trans['prev_amt'] = agg_trans['amount'].shift(1)
            for index,rows in agg_trans.iterrows():
                if index == 0:
                    agg_trans.loc[index,'available_bal'] = available_bal
                else:
                    agg_trans.loc[index, 'available_bal'] = agg_trans.loc[index-1, 'available_bal'] - agg_trans.loc[index,'prev_amt']


            agg_trans['day'] = agg_trans['date'].dt.day
            agg_trans['month_year']  = pd.to_datetime(agg_trans['date']).dt.to_period('M')

            agg_trans = agg_trans[agg_trans['date']<=min_line_date].reset_index(drop=True)

            eod_balances = pd.pivot(agg_trans,index='day',columns='month_year',values='available_bal').fillna(method='ffill')
            lastmonth_maxday = agg_trans['day'][0]
            lastmonth = agg_trans['month_year'][0]
            monthsList = list(eod_balances.columns)
            if lastmonth_maxday < 25:
                cols = list(eod_balances.columns)
                cols.remove(lastmonth)
                eod_balances_slice = eod_balances[cols].copy()
            else:
                eod_balances_slice = eod_balances.copy()

            if num_months >=6 and num_months < 12:
                eod_balances_slice = eod_balances_slice.iloc[:, -num_months:]
            else:
                eod_balances_slice = eod_balances_slice.iloc[:,-12:]

            closing_bal = eod_balances_slice.iloc[-1:,:].T
            opening_bal = closing_bal.shift(1).reset_index()
            get_first_opening_month = opening_bal[opening_bal['month_year']==opening_bal['month_year'].min()]['month_year'][0]-1
            if get_first_opening_month in eod_balances.columns:
                first_month_opening_bal = eod_balances[get_first_opening_month][-1:,].values[0]
                opening_bal.at[0,31] = first_month_opening_bal
            else:
                get_first_opening_month = opening_bal[opening_bal['month_year'] == opening_bal['month_year'].min()]['month_year'][0]
                first_month_opening_bal = eod_balances[get_first_opening_month].loc[eod_balances[get_first_opening_month].first_valid_index()]
                opening_bal.at[0, 31] = first_month_opening_bal

            closing_bal = closing_bal.reset_index()
            closing_bal.rename(columns={31:'closing_bal'},inplace=True)
            opening_bal.rename(columns={31: 'opening_bal'}, inplace=True)

            balances = pd.merge(closing_bal,opening_bal,on='month_year',how='outer')

            trans_df['debit'] = np.where(trans_df['amount']<0,trans_df['amount']*-1,np.nan)
            trans_df['credit'] = np.where(trans_df['amount']>0,trans_df['amount'],np.nan)

            total_debit = trans_df.groupby(['month_year']).agg({'debit':[np.sum,'count']}).reset_index()
            total_debit.columns = ['month_year','total_debit_amount','total_no_of_debits']
            total_credit = trans_df.groupby(['month_year']).agg({'credit': [np.sum, 'count']}).reset_index()
            total_credit.columns = ['month_year', 'total_credit_amount', 'total_no_of_credits']

            balances = pd.merge(balances,total_debit,on='month_year',how='inner')
            balances = pd.merge(balances,total_credit,on='month_year',how='inner')

            min_max_avg = pd.DataFrame()
            for col in list(balances['month_year'].values):
                vars()[col] = pd.DataFrame(eod_balances_slice[col].agg([np.min,np.max,np.mean])).T.reset_index()
                min_max_avg = min_max_avg.append(vars()[col])
            min_max_avg.rename(columns={'index':'month_year','amin':'min_eod_balance','amax':'max_eod_balance','mean':'avg_eod_balance'},inplace=True)

            balances = pd.merge(balances,min_max_avg,on='month_year',how='inner')
            # print("Hi")

            balances['month_year'] = balances['month_year'].astype(str)
            return balances

        else:
            assert (validity==True)
            # return None





        # agg_trans['available_bal'] = agg_trans['available_bal'].shift(1,fill_value=0) - agg_trans['amount'].shift(1,fill_value=0)

        # print("done")


