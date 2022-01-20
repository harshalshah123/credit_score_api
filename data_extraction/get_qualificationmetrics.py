from pymongo import MongoClient
from configs.config import conn_str,dbname
import pandas as pd
from bson import ObjectId

def get_linequalificationmetrics(user):
    client = MongoClient(conn_str)
    db = client[dbname].linequalificationmetrics
    results = db.find({"userId":{"$in":[ObjectId(user)]}})
    df = pd.DataFrame.from_records(results)
    df.columns = df.columns.str.lower()

    df['rank'] = df.groupby('userid')['createdat'].rank(ascending=False)
    df.sort_values(by=['userid', 'rank'], inplace=True)
    df = df[df['rank'] == 1]

    df1 = pd.DataFrame(df['metrics'].apply(pd.Series))
    df = df.join(df1)
    df['userid'] = df['userid'].astype(str)

    return df[['userid','liquidity','currentObligationsValue','monthlyIncome','weeklyIncome']]