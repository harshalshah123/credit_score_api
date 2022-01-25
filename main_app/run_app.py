import datetime
from configs.constants import *
import pandas as pd
import logging
import traceback
import sys
from data_extraction import get_transactions as gt,get_bankaccounts as gb,get_qualificationmetrics as gq
from services import cumulative_raw_features as crf,amount_calculation as ac
from functools import reduce
from modelling import get_score as gs
import warnings
warnings.filterwarnings('ignore')


class CREDIT_SCORE():
    def __init__(self,user_df,woe_bins,loaded_model):
        try:
            start = datetime.datetime.now()
            self.userid = user_df['userid'][0]
            self.model_score_flag = False
            self.final_df = pd.DataFrame()
            self.min_line_date = pd.to_datetime(datetime.datetime.now()) #pd.to_datetime(user_df['min_line_date'][0])

            self.sourceaccts, self.trans_df = self._extraction(self.userid,self.min_line_date)
            self.features = self._get_features()
            self.transformed_df = gs.run_model(self.features,woe_bins,loaded_model)
            self.final_df = pd.merge(self.features,self.transformed_df[['userid','score','scoreBin']],on='userid',how='left')
            self.qualification = ac.qualified_amt_calc(self.final_df)
            self.final_df = pd.merge(self.final_df,self.qualification,on='userid',how='left')
            end = datetime.datetime.now()
            print(str(end-start))
            print("Done")
            self.model_score_flag = True

        except Exception as ex:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            error = traceback.extract_tb(exc_tb)
            logging.info("Error :: %s ", str(ex.__class__) + ' == ' + str(error))
            self.model_score_flag = False
            if ex.__class__ == AssertionError:
                self.error_message = str("No Data Found...")
            elif str(ex.__class__) == "<class 'Exception'>":
                self.error_message = ex.args[0]
            else:
                self.error_message = str(ex.__class__)


    def _extraction(self,userid,min_line_date):
        logging.info("Account extraction started...")
        accounts = gb.get_all_bankaccounts(userid)

        accounts = accounts[accounts['createdat'] <= min_line_date]
        assert (len(accounts) > 0)
        sourceaccts = list(accounts['sourceaccountid'].values)
        print('sourceAccounts:' + str(sourceaccts))
        trans_df = gt._get_transactions(userid, sourceaccts)
        trans_df = pd.merge(trans_df, accounts[acct_cols], on='sourceaccountid', how='left')

        return sourceaccts, trans_df

    def _get_features(self):
        logging.info("Feature extraction started...")
        qual = gq.get_linequalificationmetrics(self.userid)
        logging.info("Balance Consolidation started...")
        master_balances = crf.get_consolidated_balances(self.trans_df, self.sourceaccts, self.min_line_date)
        assert (len(master_balances) > 0)
        logging.info("Get Raw Features started...")
        cumulative_features = crf.get_raw_features(self.userid, master_balances, 12, prefix='C1')
        logging.info("Income-Expense Features started...")
        cumulative_income, cumulative_expense = crf.cumulative_income_expense_vars(self.userid, self.trans_df, self.min_line_date,cumulative_features)
        dfs = [cumulative_features, cumulative_income, cumulative_expense,qual]
        features = reduce(lambda left, right: pd.merge(left, right, on=['userid'], how='outer'), dfs)

        features['monthlyExp'] = features[['C1M00 expense', 'C1M01 expense', 'C1M02 expense']].mean(axis=1)
        features['weeklyExp'] = features['monthlyExp'].apply(lambda x: x / 4.0)

        return features

