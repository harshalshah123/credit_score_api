from pymongo import MongoClient
from configs.config import mode,conn_str,dbname
import pandas as pd
from bson import ObjectId
import logging
import numpy as np

def _get_transactions(userid,sourceaccountids):
    try:
        # if mode == 1:
        # user = ObjectId(userid)
        client = MongoClient(conn_str)
        db = client[dbname].linetransactions
        results = db.find({"userId":{"$in":[ObjectId(userid)]}})
        df = pd.DataFrame.from_records(results)
        df.columns = df.columns.str.lower()
        df = df[df['pending'] == False]
        df = df[df['source'] == 'Plaid']
        df = df[df['sourceaccountid'].isin(sourceaccountids)]

        for col in ['markedasincome','useridentifiedas','merchantname','name','sourcecategory','dsidentifiedas','transactiontype']:
            if col not in df.columns:
                df[col] = np.nan
        # bank_accts = get_bankaccounts(user,sourceaccountid)
        # if mode ==1:
        #     df = deleted_accounts_filtering(df, bank_accts)
        #
        logging.info("Transaction Fetched..")
        # # else:
        #     pass
    except Exception as ex:
        print(ex)
        logging.info("Transaction Fetch Exception :: %s",str(ex))

    return df

# def deleted_accounts_filtering(total_transactions, total_accounts):
#
#     total_transactions = total_transactions.merge(total_accounts[['sourceaccountid','deletestatus','mask','available','current','lastbalanceupdate']], how='left', on='sourceaccountid')
#     total_transactions = total_transactions[total_transactions['deletestatus'] == 1]
#
#     print('Updated transaction shape {}'.format(total_transactions.shape))
#
#     return total_transactions
#
# def get_bankaccounts(user,sourceaccountid):
#     client = MongoClient(conn_str)
#     db = client["line_prod"].lineaccounts
#     results = db.find({"userId":{"$in":[user]}})
#     df = pd.DataFrame.from_records(results)
#     df.columns = df.columns.str.lower()
#     df = df[df['sourceaccountid'] == sourceaccountid]
#     assert len(df)>0
#     balances = df['balances'].apply(lambda x: pd.Series(x))
#     df = df.join(balances[['available', 'current']])
#
#     return df


