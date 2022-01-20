from pymongo import MongoClient
import pandas as pd
from configs.config import mode,conn_str,dbname
import pandas as pd
from bson import ObjectId
import logging
import numpy as np

def get_all_bankaccounts(user):


    client = MongoClient(conn_str)
    db = client[dbname].lineaccounts
    results = db.find({"userId":{"$in":[ObjectId(user)]}})
    df = pd.DataFrame.from_records(results)
    df.columns = df.columns.str.lower()

    assert len(df)>0
    balances = df['balances'].apply(lambda x: pd.Series(x))
    df = df.join(balances[['available', 'current']])
    df = df[df['deletestatus']==1]
    df = df[(df['accountsubtype'].isin(['checking'])) & (df['accounttype']=='depository')]
    df = df[df['source']=='plaid']
    df = df.sort_values(by=['sourceaccountid','lastbalanceupdate'],ascending=True)
    df = df.drop_duplicates(subset=['accountnumber','routingnumber','institutionid'],keep='last')

    client1 = MongoClient(conn_str)
    db = client1[dbname].lineusers
    results = db.find({"_id": {"$in": [ObjectId(user)]}})
    df1 = pd.DataFrame.from_records(results)
    df1.columns = df1.columns.str.lower()

    df1 = df1[['_id','primarybankaccount']].copy()
    df1['primary_acct_flag'] = df1.apply(lambda x: 'primary' if not pd.isnull(x['primarybankaccount']) else np.nan,axis=1)
    df1.rename(columns={"_id":'userid'},inplace=True)

    df = pd.merge(df,df1,left_on=['userid','_id'],right_on=['userid','primarybankaccount'],how='left')

    return df