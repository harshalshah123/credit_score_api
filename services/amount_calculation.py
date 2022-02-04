from configs.constants import approved_bins
import logging
import numpy as np

def qualified_amt_calc(features):
    logging.info("amt calculation started...")
    df = features.copy(deep=True)
    df['monthlyincome_multiplier'] = df.apply(lambda x: 0.70 if x['scoreBin']==1 else
                                                  0.65 if x['scoreBin']==2 else
                                                    0.6 if x['scoreBin']==3 else
                                                    0.55 if x['scoreBin']==4 else 0.5,axis=1)
    df['weeklyincome_multiplier'] = df.apply(lambda x: 0.50 if x['scoreBin'] == 1 else
                                                        0.45 if x['scoreBin'] == 2 else
                                                            0.4 if x['scoreBin'] == 3 else
                                                                0.35 if x['scoreBin'] == 4 else 0.3, axis=1)
    df['biweeklyInstallment'] = df.apply(lambda x: ((x['monthlyIncome']*x['monthlyincome_multiplier'])+x['monthlyExp'])/2.0,axis=1)
    df['weeklyInstallment'] = df.apply(lambda x: (x['weeklyIncome']*x['weeklyincome_multiplier'])+x['weeklyExp'],axis=1)

    df['monthlyQualifiedAmt'] = df.apply(lambda x: 0 if x['biweeklyInstallment'] < 0 else x['biweeklyInstallment']*6,axis=1)
    df['weeklyQualifiedAmt'] = df.apply(lambda x: 0 if x['weeklyInstallment'] < 0 else x['weeklyInstallment'],axis=1)

    df['monthlyQualifiedAmt_1'] = df.apply(lambda x:0 if (x['biweeklyInstallment']<0 or x['weeklyInstallment']<0) else x['monthlyQualifiedAmt'],axis=1)
    df['weeklyQualifiedAmt_1'] = df.apply(lambda x:40 if (x['biweeklyInstallment']<0 or x['weeklyInstallment']<0) else x['weeklyQualifiedAmt'],axis=1)

    df['monthlyQual'] = df.apply(lambda x: 150 if x['monthlyQualifiedAmt_1']>150 else round(x['monthlyQualifiedAmt_1'],-1),axis=1)
    df['weeklyQual'] = df.apply(lambda x: 100 if x['weeklyQualifiedAmt_1']>100 else
                                          40 if (round(x['weeklyQualifiedAmt_1'],-1) == 0 and x['weeklyQualifiedAmt_1'] >0) else round(x['weeklyQualifiedAmt_1'],-1),axis=1)

    df['min_qual'] = df[['monthlyQual','weeklyQual']].min(axis=1)
    df['max_qual'] = df[['monthlyQual','weeklyQual']].max(axis=1)
    df['max_qual'] = df.apply(lambda x: abs(x['primaryLenders_avg_debt_amt_1m']) if (x['max_qual'] > abs(x['primaryLenders_avg_debt_amt_1m']) and abs(x['primaryLenders_avg_debt_amt_1m']) > 0) else x['max_qual'],axis=1)

    df['qualified_plan'] = df.apply(lambda x: 'Not-qualified' if ((x['monthlyQual']==0 and x['weeklyQual']==0) or x['scoreBin'] not in approved_bins ) else
                                                'Micro' if x['max_qual']<=100 else
                                                'Medium' if x['max_qual']>100 else 'Not-qualified',axis=1)

    df['micro_qualified_amt'] = df.apply(lambda x: 40 if (x['qualified_plan']=='Micro' and x['max_qual']<40) else
                                                    x['max_qual'] if (x['qualified_plan']=='Micro' and x['max_qual']>40) else
                                                    40 if (x['qualified_plan']=='Medium' and x['min_qual']<40) else
                                                    x['min_qual'] if (x['qualified_plan'] == 'Medium' and x['min_qual'] > 40) else 0,axis=1)

    df['medium_qualified_amt'] = df.apply(lambda x: x['max_qual'] if x['qualified_plan']=='Medium' else 0,axis=1)

    df['micro_qualified_amt'] = df['micro_qualified_amt'].round(-1)
    df['medium_qualified_amt'] = df['medium_qualified_amt'].round(-1)

    df['micro_qualified_amt'] = np.where(df['micro_qualified_amt']>100,100,df['micro_qualified_amt'])
    # df['medium_qualified_amt'] = np.where(df['medium_qualified_amt']>150,150,df['medium_qualified_amt'])
    df['medium_qualified_amt'] = np.where(df['qualified_plan']=='Medium',150,df['medium_qualified_amt'])

    return df[['userid','qualified_plan','micro_qualified_amt','medium_qualified_amt','min_qual','max_qual']]