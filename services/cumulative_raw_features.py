import pandas as pd

from configs.constants import *
from services.utils import *
from services import balance_calculate as bc
from services import derived_features as df
from services import get_incometype as gi
from functools import reduce
import calendar
import warnings
warnings.filterwarnings('ignore')

def get_consolidated_balances(trans_df,sourceaccts,min_line_date):
    master_balances = pd.DataFrame()
    cnt = 0
    for acct in sourceaccts:
        trans_slice = trans_df[trans_df['sourceaccountid'] == acct]
        trans_slice.reset_index(drop=True, inplace=True)
        min_date = trans_df['lastbalanceupdate'][0] if min_line_date == '' else min_line_date
        primary_flag = trans_slice['primary_acct_flag'][0]
        try:
            balances = bc.BALANCE()._get_balances(trans_slice, min_date)
            balances['sourceaccountid'] = acct
            balances['primary_acct_flag'] = primary_flag
        # balances['acct_flag'] = 'B' + str(cnt)
            master_balances = master_balances.append(balances)
        except:
            continue
        cnt += 1

    return master_balances


def get_raw_features(userid,master_balances,no_of_months,prefix):
    tmp = master_balances.copy()

    # del tmp['acct_flag']
    cumulatives = tmp.groupby('month_year').sum().reset_index()
    cumulatives.sort_values(by='month_year', ascending=False, inplace=True)
    cumulatives.reset_index(inplace=True,drop=True)
    # del cumulatives['index']
    cumulatives.reset_index(inplace=True)
    cumulatives['mno'] = cumulatives.apply(lambda x: prefix+'M' + str('0' + str(int(x['index'])) if int(x['index']) < 10 else str(int(x['index']))), axis=1)
    del cumulatives['index']
    cumulatives = cumulatives.head(12)
    cumulatives.rename(columns=new_cols, inplace=True)
    cumulatives['userid'] = userid
    cumulative_features = pivot_processing(cumulatives, indexcol='userid')
    # if prefix == 'C1':
    #     cumulative_features['no_of_months_of_bs'] = no_of_months

    # cum_credit_vars = month_vars_name('Credits',prefix)
    # # cum_net_inflow_vars = month_vars_name('Net Inflow',prefix)
    # for var in cum_credit_vars:
    #     colprefix = var[0:6]
    #     if var in cumulative_features.columns:
    #         cumulative_features[colprefix + 'Net flow'] = cumulative_features[var] - cumulative_features[colprefix + 'Debits']
    #         cumulative_features[colprefix + 'CrDrR'] = cumulative_features[var]/(cumulative_features[colprefix + 'Debits'])
    #     else:
    #         cumulative_features[colprefix + 'Net flow'] = np.nan
    #         cumulative_features[colprefix + 'CrDrR'] = np.nan

    if prefix=='C1':
        for col in cum_master_cols:
            if col not in list(cumulative_features.columns):
                cumulative_features[col] = np.nan
    elif prefix=='B0':
        for col in primary_master_cols:
            if col not in list(cumulative_features.columns):
                cumulative_features[col] = np.nan

    cumulative_features = df.cov_calc(cumulative_features,prefix,6)
    # cumulative_features = df.get_timely_variables(cumulative_features,prefix)
    # cumulative_features = df.get_growth_variables(cumulative_features,prefix)

    return cumulative_features

def cumulative_income_expense_vars(userid,trans_df,min_line_date,cumulative_features):
    incomeObj = gi.INCOME_TYPE(trans_df, min_line_date)
    income_trans = incomeObj.income_trans.copy(deep=True)
    expense_trans = incomeObj.expense_trans.copy(deep=True)
    trans_filtered = incomeObj.trans.copy(deep=True)

    income_trans['month_year'] = pd.to_datetime(income_trans['date']).dt.to_period('M')
    expense_trans['month_year'] = pd.to_datetime(expense_trans['date']).dt.to_period('M')

    aggIncome = income_trans.groupby(['month_year']).agg({'amount': np.sum}).reset_index()
    aggExpense = expense_trans.groupby(['month_year']).agg({'amount': np.sum}).reset_index()
    aggIncome['month_year'] = aggIncome['month_year'].astype(str)
    aggExpense['month_year'] = aggExpense['month_year'].astype(str)

    mnolist = month_vars_name('month_year', 'C1')
    cum_tmp = cumulative_features[mnolist].T.reset_index()

    cumulativeIncome = get_income_features(userid,aggIncome,cum_tmp,trans_filtered)
    cumulativeExpense = get_expense_features(userid,aggExpense,cum_tmp)

    cumulativeIncome = get_no_of_unique_lenders(trans_filtered,min_line_date,cumulativeIncome)

    categorized_expenses = get_categorized_expenses(userid,trans_filtered,cum_tmp)
    cumulativeExpense = pd.merge(cumulativeExpense,categorized_expenses,on='userid',how='left')

    return cumulativeIncome,cumulativeExpense


def get_categorized_expenses(userid,trans,cum_tmp):
    # print("entered categorized Expense...")
    trans['transactioncategory'] = trans['transactioncategory'].astype(str)
    trans['month_year'] = pd.to_datetime(trans['date']).dt.to_period('M').astype(str)

    # travel_exp = trans[(trans['transactioncategory']=='5e9972aa7cd42a3bfc5d3b89')& (trans['amount']<0)]
    # subscription_exp = trans[(trans['transactioncategory']=='5e9972aa7cd42a3bfc5d3b81')& (trans['amount']<0)]
    # utility_exp = trans[(trans['transactioncategory']=='5e9972aa7cd42a3bfc5d3b91')& (trans['amount']<0)]
    # primary_exp = trans[(trans['transactioncategory'].isin(primary_exp_categories)) & (trans['amount']<0)]
    secondary_exp = trans[(trans['transactioncategory'].isin(secondary_exp_categories)) & (trans['amount']<0)]

    # if len(travel_exp) > 0:
    #     aggTravel = travel_exp.groupby(['month_year']).agg({'amount': np.sum}).reset_index()
    #     aggTravel = pd.merge(cum_tmp, aggTravel, left_on=0, right_on='month_year', how='left')
    #     aggTravel['userid'] = userid
    #     aggTravel['index'] = aggTravel['index'].str.replace('month_year', 'travel exp')
    #     aggTravel['amount'] = aggTravel['amount'].fillna(0)
    #     cumulativeTravel = aggTravel.pivot(index='userid', columns='index', values='amount').reset_index()
    #
    # else:
    #     cumulativeTravel=pd.DataFrame({'userid':[userid]})
    #
    # if len(subscription_exp) > 0:
    #     aggSubscriptions = subscription_exp.groupby(['month_year']).agg({'amount': np.sum}).reset_index()
    #     aggSubscriptions = pd.merge(cum_tmp, aggSubscriptions, left_on=0, right_on='month_year', how='left')
    #     aggSubscriptions['userid'] = userid
    #     aggSubscriptions['index'] = aggSubscriptions['index'].str.replace('month_year', 'subscription exp')
    #     aggSubscriptions['amount'] = aggSubscriptions['amount'].fillna(0)
    #     cumulativeSubscriptions = aggSubscriptions.pivot(index='userid', columns='index', values='amount').reset_index()
    #
    # else:
    #     cumulativeSubscriptions = pd.DataFrame({'userid':[userid]})
    #
    # if len(utility_exp) > 0:
    #     aggUtility = utility_exp.groupby(['month_year']).agg({'amount': np.sum}).reset_index()
    #     aggUtility = pd.merge(cum_tmp, aggUtility, left_on=0, right_on='month_year', how='left')
    #     aggUtility['userid'] = userid
    #     aggUtility['index'] = aggUtility['index'].str.replace('month_year', 'utility exp')
    #     aggUtility['amount'] = aggUtility['amount'].fillna(0)
    #     cumulativeUtility = aggUtility.pivot(index='userid', columns='index', values='amount').reset_index()
    #
    # else:
    #     cumulativeUtility = pd.DataFrame({'userid':[userid]})
    #
    # if len(primary_exp) > 0:
    #     aggPrimary = primary_exp.groupby(['month_year']).agg({'amount': np.sum}).reset_index()
    #     aggPrimary = pd.merge(cum_tmp, aggPrimary, left_on=0, right_on='month_year', how='left')
    #     aggPrimary['userid'] = userid
    #     aggPrimary['index'] = aggPrimary['index'].str.replace('month_year', 'primary exp')
    #     aggPrimary['amount'] = aggPrimary['amount'].fillna(0)
    #     cumulativePrimary = aggPrimary.pivot(index='userid', columns='index', values='amount').reset_index()
    #
    # else:
    #     cumulativePrimary = pd.DataFrame({'userid':[userid]})


    if len(secondary_exp) > 0:
        aggSecondary = secondary_exp.groupby(['month_year']).agg({'amount': np.sum}).reset_index()
        aggSecondary = pd.merge(cum_tmp, aggSecondary, left_on=0, right_on='month_year', how='left')
        aggSecondary['userid'] = userid
        aggSecondary['index'] = aggSecondary['index'].str.replace('month_year', 'secondary exp')
        aggSecondary['amount'] = aggSecondary['amount'].fillna(0)
        cumulativeSecondary = aggSecondary.pivot(index='userid', columns='index', values='amount').reset_index()

    else:
        cumulativeSecondary = pd.DataFrame({'userid':[userid]})

    # dfs = [cumulativePrimary,cumulativeSecondary,cumulativeSubscriptions,cumulativeUtility,cumulativeTravel]
    # categorized_expeses = reduce(lambda left, right: pd.merge(left, right, on=['userid'], how='outer'), dfs)
    categorized_expeses = cumulativeSecondary.copy(deep=True)


    cols = ['C1M00 secondary exp','C1M01 secondary exp','C1M02 secondary exp','C1M03 secondary exp','C1M04 secondary exp','C1M05 secondary exp','C1M06 secondary exp','C1M07 secondary exp','C1M08 secondary exp','C1M09 secondary exp','C1M10 secondary exp','C1M11 secondary exp'] #'C1M00 primary exp','C1M01 primary exp','C1M02 primary exp','C1M03 primary exp','C1M04 primary exp','C1M05 primary exp','C1M06 primary exp','C1M07 primary exp','C1M08 primary exp','C1M09 primary exp','C1M10 primary exp','C1M11 primary exp',,'C1M00 subscription exp','C1M01 subscription exp','C1M02 subscription exp','C1M03 subscription exp','C1M04 subscription exp','C1M05 subscription exp','C1M06 subscription exp','C1M07 subscription exp','C1M08 subscription exp','C1M09 subscription exp','C1M10 subscription exp','C1M11 subscription exp','C1M00 utility exp','C1M01 utility exp','C1M02 utility exp','C1M03 utility exp','C1M04 utility exp','C1M05 utility exp','C1M06 utility exp','C1M07 utility exp','C1M08 utility exp','C1M09 utility exp','C1M10 utility exp','C1M11 utility exp','C1M00 travel exp','C1M01 travel exp','C1M02 travel exp','C1M03 travel exp','C1M04 travel exp','C1M05 travel exp','C1M06 travel exp','C1M07 travel exp','C1M08 travel exp','C1M09 travel exp','C1M10 travel exp','C1M11 travel exp'
    for col in cols:
        if col not in list(categorized_expeses.columns):
            categorized_expeses[col] = 0.0

    # categorized_expeses['last3m_avg_travel_exp'] = categorized_expeses[['C1M00 travel exp','C1M01 travel exp','C1M02 travel exp']].mean(axis=1)
    # categorized_expeses['last3m_avg_utility_exp'] = categorized_expeses[['C1M00 utility exp','C1M01 utility exp','C1M02 utility exp']].mean(axis=1)
    # categorized_expeses['last3m_avg_subscription_exp'] = categorized_expeses[['C1M00 subscription exp','C1M01 subscription exp','C1M02 subscription exp']].mean(axis=1)
    # categorized_expeses['last3m_avg_primary_exp'] = categorized_expeses[['C1M00 primary exp','C1M01 primary exp','C1M02 primary exp']].mean(axis=1)
    # categorized_expeses['last3m_avg_secondary_exp'] = categorized_expeses[['C1M00 secondary exp','C1M01 secondary exp','C1M02 secondary exp']].mean(axis=1)
    #
    # categorized_expeses['last6m_avg_travel_exp'] = categorized_expeses[['C1M00 travel exp','C1M01 travel exp','C1M02 travel exp','C1M03 travel exp','C1M04 travel exp','C1M05 travel exp']].mean(axis=1)
    # categorized_expeses['last6m_avg_utility_exp'] = categorized_expeses[['C1M00 utility exp','C1M01 utility exp','C1M02 utility exp','C1M03 utility exp','C1M04 utility exp','C1M05 utility exp']].mean(axis=1)
    # categorized_expeses['last6m_avg_subscription_exp'] = categorized_expeses[['C1M00 subscription exp','C1M01 subscription exp','C1M02 subscription exp','C1M03 subscription exp','C1M04 subscription exp','C1M05 subscription exp']].mean(axis=1)
    # categorized_expeses['last6m_avg_primary_exp'] = categorized_expeses[['C1M00 primary exp','C1M01 primary exp','C1M02 primary exp','C1M03 primary exp','C1M04 primary exp','C1M05 primary exp']].mean(axis=1)
    # categorized_expeses['last6m_avg_secondary_exp'] = categorized_expeses[['C1M00 secondary exp','C1M01 secondary exp','C1M02 secondary exp','C1M03 secondary exp','C1M04 secondary exp','C1M05 secondary exp']].mean(axis=1)

    return categorized_expeses

def get_income_features(userid,aggIncome,cum_tmp,trans):
    # aggIncome['2MEWM_income'] = aggIncome['amount'].ewm(span=2, adjust=False).mean()
    # aggIncome['3MEWM_income'] = aggIncome['amount'].ewm(span=3, adjust=False).mean()
    # aggIncome['6MEWM_income'] = aggIncome['amount'].ewm(span=6, adjust=False).mean()
    # incomeSignal_last6m = extractSignal_kalmanFiltering(aggIncome['account'][-6:])

    aggIncome = pd.merge(cum_tmp, aggIncome, left_on=0, right_on='month_year', how='left')
    aggIncome['userid'] = userid
    aggIncome['index'] = aggIncome['index'].str.replace('month_year', 'income')
    cumulativeIncome = aggIncome.pivot(index='userid', columns='index', values='amount').reset_index()
    # aggIncome['index'] = aggIncome['index'].str.replace('income', '2MEWM_income')
    # cumulative_2EWM_Income = aggIncome.pivot(index='userid', columns='index', values='2MEWM_income').reset_index()
    # aggIncome['index'] = aggIncome['index'].str.replace('2MEWM_income', '3MEWM_income')
    # cumulative_3EWM_Income = aggIncome.pivot(index='userid', columns='index', values='3MEWM_income').reset_index()
    # aggIncome['index'] = aggIncome['index'].str.replace('3MEWM_income', '6MEWM_income')
    # cumulative_6EWM_Income = aggIncome.pivot(index='userid', columns='index', values='6MEWM_income').reset_index()
    #
    # cumulativeIncome = pd.merge(cumulativeIncome, cumulative_2EWM_Income, on='userid', how='left')
    # cumulativeIncome = pd.merge(cumulativeIncome, cumulative_3EWM_Income, on='userid', how='left')
    # cumulativeIncome = pd.merge(cumulativeIncome, cumulative_6EWM_Income, on='userid', how='left')

    cumulativeIncome = cumulativeIncome.fillna(0)
    # cumulativeIncome['C1_3mAvgIncome'] = cumulativeIncome[['C1M00 income', 'C1M01 income', 'C1M02 income']].mean(axis=1)
    # cumulativeIncome['C1_6mAvgIncome'] = cumulativeIncome[['C1M00 income', 'C1M01 income', 'C1M02 income', 'C1M03 income', 'C1M04 income', 'C1M05 income']].mean(axis=1)
    # cumulativeIncome['C1_3mIncomeGrowth'] = np.where(cumulativeIncome['C1M02 income'] == 0, np.nan, ((cumulativeIncome['C1M00 income'] / cumulativeIncome['C1M02 income']) - 1))
    # cumulativeIncome['C1_6mIncomeGrowth'] = np.where(cumulativeIncome['C1M05 income'] == 0, np.nan, ((cumulativeIncome['C1M00 income'] / cumulativeIncome['C1M05 income']) - 1))
    #
    # cumulativeIncome = get_useridentifiedIncome_features(userid,trans,cum_tmp,cumulativeIncome)
    #
    # userincome_cols = month_vars_name('useridentified income',prefix='C1')

    # for col in userincome_cols:
    #     if col not in cumulativeIncome.columns:
    #         cumulativeIncome[col] = np.nan

    return cumulativeIncome

def get_useridentifiedIncome_features(userid,trans,cum_tmp,cumulativeIncome):
    trans['month_year'] = pd.to_datetime(trans['date']).dt.to_period('M').astype(str)
    trans['month_year'] = trans['month_year'].astype(str)
    useridentified_income = trans[(trans['useridentifiedas'] == 'income') & (trans['amount'] > 0)]

    if len(useridentified_income) > 0:
        aggUserIncome = useridentified_income.groupby('month_year').agg({'amount': np.sum}).reset_index()
        aggUserIncome = pd.merge(cum_tmp, aggUserIncome, left_on=0, right_on='month_year', how='left')
        aggUserIncome['userid'] = userid
        aggUserIncome['index'] = aggUserIncome['index'].str.replace('month_year', 'useridentified income')
        aggUserIncome['amount'] = aggUserIncome['amount'].fillna(0)
        cumulativeUserIncome = aggUserIncome.pivot(index='userid', columns='index', values='amount').reset_index()
    else:
        cumulativeUserIncome = pd.DataFrame()

    if len(cumulativeUserIncome) > 0:
        cumulativeIncome = pd.merge(cumulativeIncome, cumulativeUserIncome, on='userid', how='left')

    return cumulativeIncome

def get_expense_features(userid,aggExpense,cum_tmp):
    aggExpense = pd.merge(cum_tmp, aggExpense, left_on=0, right_on='month_year', how='left')
    aggExpense['index'] = aggExpense['index'].str.replace('month_year', 'expense')
    aggExpense['userid'] = userid
    cumulativeExpense = aggExpense.pivot(index='userid', columns='index', values='amount').reset_index()
    cumulativeExpense = cumulativeExpense.fillna(0)
    # cumulativeExpense['C1_3mAvgExpense'] = cumulativeExpense[['C1M00 expense', 'C1M01 expense', 'C1M02 expense']].mean(axis=1)
    # cumulativeExpense['C1_6mAvgExpense'] = cumulativeExpense[['C1M00 expense', 'C1M01 expense', 'C1M02 expense', 'C1M03 expense', 'C1M04 expense', 'C1M05 expense']].mean(axis=1)
    # cumulativeExpense['C1_3mExpenseGrowth'] = np.where(cumulativeExpense['C1M02 expense'] == 0, np.nan, ((cumulativeExpense['C1M00 expense'] / cumulativeExpense['C1M02 expense']) - 1))
    # cumulativeExpense['C1_6mExpenseGrowth'] = np.where(cumulativeExpense['C1M05 expense'] == 0, np.nan, ((cumulativeExpense['C1M00 expense'] / cumulativeExpense['C1M05 expense']) - 1))

    return cumulativeExpense

def get_no_of_unique_lenders(trans_df,min_line_date,cumulativeIncome):
    loans_cat = ["5e9972aa7cd42a3bfc5d3b90", "5e9972aa7cd42a3bfc5d3b7e"]  ##Loans ##Mortages
    loans_cat = [str(x) for x in loans_cat]
    trans_df = trans_df[(trans_df["transactioncategory"].astype("str").isin(loans_cat)) | (trans_df["sourcecategories"].apply(lambda x: "Loans and Mortgages" in x))]
    total_outflow = trans_df[trans_df["amount"] <= -10]
    last1m_date = min_line_date - pd.offsets.DateOffset(months=1)
    last3m_date = min_line_date - pd.offsets.DateOffset(months=3)
    last6m_date = min_line_date - pd.offsets.DateOffset(months=6)
    total_outflow1m = total_outflow[total_outflow["date"] >= last1m_date]
    total_outflow3m = total_outflow[total_outflow["date"] >= last3m_date]
    # total_outflow6m = total_outflow[total_outflow["date"] >= last6m_date]

    if len(total_outflow1m) >0:
        no_of_unique_lenders_1m = len(total_outflow1m['merchantname'].unique().tolist())
        avg_debt_amt_1m = float(total_outflow1m['amount'].sum())/no_of_unique_lenders_1m
        total_outflow1m['primary_lenders_flag'] = total_outflow1m.apply(lambda x: 1 if any(word in x['merchantname'].lower() for word in ['albert', 'earnin', 'dave', 'brigit']) else 0,axis=1)
        total_outflow1m['competitors_flag'] = total_outflow1m.apply(lambda x: 1 if any(word in x['merchantname'].lower() for word in ['affirm','sezzle','afterpay','spilitit','perpay','paypal','klarna']) else 0,axis=1)

        primary_lenderdebt_1m = total_outflow1m[total_outflow1m['primary_lenders_flag']==1].groupby('userid').agg({'amount':[np.sum,np.mean]}).reset_index()
        # competitor_debt_1m = total_outflow1m[total_outflow1m['competitors_flag'] == 1].groupby('userid').agg({'amount': [np.sum,np.mean]}).reset_index()


        if len(primary_lenderdebt_1m)>0:
            primary_lenderdebt_1m.columns = ['userid','primaryLenders_total_debt_1m','primaryLenders_avg_debt_amt_1m']
            primaryLenders_avg_debt_amt_1m = primary_lenderdebt_1m['primaryLenders_avg_debt_amt_1m'][0]
            primaryLenders_total_debt_1m = primary_lenderdebt_1m['primaryLenders_total_debt_1m'][0]
        else:
            primaryLenders_avg_debt_amt_1m = 0
            primaryLenders_total_debt_1m = 0

        # if len(competitor_debt_1m)>0:
        #     competitor_debt_1m.columns = ['userid','competitor_total_debt_1m','competitor_avg_debt_amt_1m']
        #     competitor_avg_debt_amt_1m = competitor_debt_1m['competitor_avg_debt_amt_1m'][0]
        #     competitor_total_debt_1m = competitor_debt_1m['competitor_total_debt_1m'][0]
        # else:
        #     competitor_avg_debt_amt_1m = 0
        #     competitor_total_debt_1m = 0
    else:
        no_of_unique_lenders_1m = 0
        avg_debt_amt_1m = 0
        primaryLenders_avg_debt_amt_1m = 0
        primaryLenders_total_debt_1m = 0
        # competitor_avg_debt_amt_1m = 0
        # competitor_total_debt_1m = 0

    if len(total_outflow3m) >0:
        no_of_unique_lenders_3m = len(total_outflow3m['merchantname'].unique().tolist())
        avg_debt_amt_3m = float(total_outflow3m['amount'].sum())/no_of_unique_lenders_3m

        total_outflow3m['primary_lenders_flag'] = total_outflow3m.apply(lambda x: 1 if any(word in x['merchantname'].lower() for word in ['albert', 'earnin', 'dave', 'brigit']) else 0, axis=1)
        total_outflow3m['competitors_flag'] = total_outflow3m.apply(lambda x: 1 if any(word in x['merchantname'].lower() for word in ['affirm', 'sezzle', 'afterpay', 'spilitit', 'perpay', 'paypal', 'klarna']) else 0, axis=1)

        primary_lenderdebt_3m = total_outflow3m[total_outflow3m['primary_lenders_flag'] == 1].groupby('userid').agg({'amount': [np.sum,np.mean]}).reset_index()
        # competitor_debt_3m = total_outflow3m[total_outflow3m['competitors_flag'] == 1].groupby('userid').agg({'amount': [np.sum,np.mean]}).reset_index()

        if len(primary_lenderdebt_3m) > 0:
            primary_lenderdebt_3m.columns = ['userid','primaryLenders_total_debt_3m','primaryLenders_avg_debt_amt_3m']
            primaryLenders_avg_debt_amt_3m = primary_lenderdebt_3m['primaryLenders_avg_debt_amt_3m'][0]
            primaryLenders_total_debt_3m = primary_lenderdebt_3m['primaryLenders_total_debt_3m'][0]
        else:
            primaryLenders_avg_debt_amt_3m = 0
            primaryLenders_total_debt_3m = 0

        # if len(competitor_debt_3m) > 0:
        #     competitor_debt_3m.columns = ['userid', 'competitor_total_debt_3m', 'competitor_avg_debt_amt_3m']
        #     competitor_avg_debt_amt_3m = competitor_debt_3m['competitor_avg_debt_amt_3m'][0]
        #     competitor_total_debt_3m = competitor_debt_3m['competitor_total_debt_3m'][0]
        # else:
        #     competitor_avg_debt_amt_3m = 0
        #     competitor_total_debt_3m = 0
    else:
        no_of_unique_lenders_3m = 0
        avg_debt_amt_3m = 0
        primaryLenders_avg_debt_amt_3m = 0
        primaryLenders_total_debt_3m = 0
        # competitor_avg_debt_amt_3m = 0
        # competitor_total_debt_3m = 0

    # if len(total_outflow6m) >0:
    #     no_of_unique_lenders_6m = len(total_outflow6m['merchantname'].unique().tolist())
    #     avg_debt_amt_6m = float(total_outflow6m['amount'].sum()) / no_of_unique_lenders_6m
    #     total_outflow6m['primary_lenders_flag'] = total_outflow6m.apply(lambda x: 1 if any(word in x['merchantname'].lower() for word in ['albert', 'earnin', 'dave', 'brigit']) else 0, axis=1)
    #     total_outflow6m['competitors_flag'] = total_outflow6m.apply(lambda x: 1 if any(word in x['merchantname'].lower() for word in ['affirm', 'sezzle', 'afterpay', 'spilitit', 'perpay', 'paypal', 'klarna']) else 0, axis=1)
    #
    #     primary_lenderdebt_6m = total_outflow6m[total_outflow6m['primary_lenders_flag'] == 1].groupby('userid').agg({'amount': [np.sum,np.mean]}).reset_index()
    #     competitor_debt_6m = total_outflow6m[total_outflow6m['competitors_flag'] == 1].groupby('userid').agg({'amount': [np.sum,np.mean]}).reset_index()
    #
    #     if len(primary_lenderdebt_6m) > 0:
    #         primary_lenderdebt_6m.columns = ['userid', 'primaryLenders_total_debt_6m', 'primaryLenders_avg_debt_amt_6m']
    #         primaryLenders_avg_debt_amt_6m = primary_lenderdebt_6m['primaryLenders_avg_debt_amt_6m'][0]
    #         primaryLenders_total_debt_6m = primary_lenderdebt_6m['primaryLenders_total_debt_6m'][0]
    #     else:
    #         primaryLenders_avg_debt_amt_6m = 0
    #         primaryLenders_total_debt_6m = 0
    #
    #     if len(competitor_debt_6m) > 0:
    #         competitor_debt_6m.columns = ['userid', 'competitor_total_debt_6m', 'competitor_avg_debt_amt_6m']
    #         competitor_avg_debt_amt_6m = competitor_debt_6m['competitor_avg_debt_amt_6m'][0]
    #         competitor_total_debt_6m = competitor_debt_6m['competitor_total_debt_6m'][0]
    #     else:
    #         competitor_avg_debt_amt_6m = 0
    #         competitor_total_debt_6m = 0
    # else:
    #     no_of_unique_lenders_6m = 0
    #     avg_debt_amt_6m = 0
    #     primaryLenders_avg_debt_amt_6m = 0
    #     competitor_avg_debt_amt_6m = 0
    #     primaryLenders_total_debt_6m = 0
    #     competitor_total_debt_6m = 0

    cumulativeIncome['no_of_unique_lenders_1m'] = no_of_unique_lenders_1m
    cumulativeIncome['no_of_unique_lenders_3m'] = no_of_unique_lenders_3m
    # cumulativeIncome['no_of_unique_lenders_6m'] = no_of_unique_lenders_6m
    cumulativeIncome['avg_debt_amt_1m'] = avg_debt_amt_1m
    cumulativeIncome['avg_debt_amt_3m'] = avg_debt_amt_3m
    # cumulativeIncome['avg_debt_amt_6m'] = avg_debt_amt_6m
    # cumulativeIncome['primaryLenders_avg_debt_amt_6m'] = primaryLenders_avg_debt_amt_6m
    cumulativeIncome['primaryLenders_avg_debt_amt_3m'] = primaryLenders_avg_debt_amt_3m
    cumulativeIncome['primaryLenders_avg_debt_amt_1m'] = primaryLenders_avg_debt_amt_1m
    # cumulativeIncome['primaryLenders_total_debt_amt_6m'] = primaryLenders_total_debt_6m
    cumulativeIncome['primaryLenders_total_debt_amt_3m'] = primaryLenders_total_debt_3m
    cumulativeIncome['primaryLenders_total_debt_amt_1m'] = primaryLenders_total_debt_1m
    #
    # cumulativeIncome['competitor_avg_debt_amt_6m'] = competitor_avg_debt_amt_6m
    # cumulativeIncome['competitor_avg_debt_amt_3m'] = competitor_avg_debt_amt_3m
    # cumulativeIncome['competitor_avg_debt_amt_1m'] = competitor_avg_debt_amt_1m
    # cumulativeIncome['competitor_total_debt_amt_6m'] = competitor_total_debt_6m
    # cumulativeIncome['competitor_total_debt_amt_3m'] = competitor_total_debt_3m
    # cumulativeIncome['competitor_total_debt_amt_1m'] = competitor_total_debt_1m
    #

    return cumulativeIncome

def income_over_revenues(features):
    vars_for_loop = month_vars_name('Credits',prefix='C1')

    for var in vars_for_loop:
        prefix = var[0:6]
        features[prefix + 'income over revenue'] = np.where(features[var]==0,np.nan,features[prefix + 'income']/features[var])
        features[prefix + 'user_income over revenue'] = np.where(features[var]==0,np.nan,features[prefix + 'useridentified income']/features[var])

    return features

def get_credit_transactions_gap(userid,trans_df,min_line_date):
    trans_df['month_year'] = pd.to_datetime(trans_df['date']).dt.to_period('M')
    trans_df = trans_df.sort_values(by='date', ascending=False)
    trans_df = trans_df[trans_df['date']<=min_line_date]
    trans_df = trans_df.reset_index(drop=True)

    lastmonth_maxday = trans_df['date'].max().day
    lastmonth = trans_df['month_year'][0]

    if lastmonth_maxday < 25:
        trans_df = trans_df[trans_df['month_year'] != lastmonth]

    credit_df = trans_df[trans_df['amount']>0]
    credit_df = credit_df[['userid','date','amount']]
    aggCredit = credit_df.groupby('date').agg({'amount':np.sum}).reset_index()

    aggCredit['day'] = aggCredit['date'].dt.day
    aggCredit['month_year'] = pd.to_datetime(aggCredit['date']).dt.to_period('M')

    aggCredit = aggCredit[aggCredit['date'] <= min_line_date].reset_index(drop=True)
    aggCredit = aggCredit.sort_values(by='date',ascending=False)
    aggCredit.reset_index(drop=True,inplace=True)

    last_credit_dt = aggCredit['date'][0]
    last_month = aggCredit['month_year'][0]
    mindate,maxdate = get_month_day_range(last_credit_dt)
    # all_days = pd.date_range(aggCredit['date'].min(), aggCredit['date'].max(), freq='D')
    aggCredit_1m = aggCredit[aggCredit['month_year']==last_month]
    aggCredit_1m['date'] = pd.to_datetime(aggCredit_1m['date'])
    # aggCredit_1m.set_index('date',inplace=True)
    idx = pd.DataFrame(pd.date_range(mindate, maxdate))
    aggCredit_1m = pd.merge(idx,aggCredit_1m,left_on=0,right_on='date',how='left')
    aggCredit_1m['amount'] = aggCredit_1m['amount'].fillna(0)
    aggCredit_1m['gap'] = np.where(aggCredit_1m['amount']==0,1,0)

    avg_cr_trans_gap_1m = aggCredit_1m['gap'].mean()


    periods_3m = list(aggCredit['month_year'].unique())[0:3]
    aggCredit_3m = aggCredit[aggCredit['month_year'].isin(periods_3m)]
    aggCredit_3m['date'] = pd.to_datetime(aggCredit_1m['date'])
    last_credit_dt_3m = maxdate - datetime.timedelta(days = 90)
    mindate_3m, maxdate_3m = get_month_day_range(last_credit_dt_3m)
    idx1 = pd.DataFrame(pd.date_range(mindate_3m, maxdate))

    aggCredit_3m = pd.merge(idx1, aggCredit_3m, left_on=0, right_on='date', how='left')
    aggCredit_3m['amount'] = aggCredit_3m['amount'].fillna(0)
    aggCredit_3m['gap'] = np.where(aggCredit_3m['amount'] == 0, 1, 0)

    avg_cr_trans_gap_3m = aggCredit_3m['gap'].mean()

    cr_gap_df = pd.DataFrame({'userid':[userid]})
    cr_gap_df['avg_cr_trans_gap_1m'] = avg_cr_trans_gap_1m
    cr_gap_df['avg_cr_trans_gap_3m'] = avg_cr_trans_gap_3m


    return cr_gap_df



    # aggCredit_1m = aggCredit_1m.reindex(idx, fill_value=0)
