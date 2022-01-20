from pymongo import MongoClient
import pandas as pd
from configs.config import mode,conn_str,dbname
import pandas as pd
from bson import ObjectId
import logging
import numpy as np


def get_min_loandate(user):

    client = MongoClient(conn_str)
    db = client[dbname].linesubscriptions
    results = db.find({"userId":{"$in":[ObjectId(user)]}})
    df = pd.DataFrame.from_records(results)
    df.columns = df.columns.str.lower()
    if len(df)>0:
        agg = df.groupby('userid').agg({'createdat':np.min}).reset_index()
        min_line_date = agg['createdat'][0]
    else:
        min_line_date = ''

    return min_line_date

def get_min_accountLinked_date(df):

    agg = df.groupby('userid').agg({'createdat':np.min}).reset_index()
    min_line_date = agg['createdat'][0]

    return min_line_date
