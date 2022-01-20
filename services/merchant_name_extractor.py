# import numba
import string
from services.merchant_match import initial_merchant_check, text_cleanup
from configs.merchant_list import merchant_list_map,keywords_removal
from rapidfuzz import fuzz
import pandas as pd
import numpy as np

# @numba.jit
def get_merchant_name(name,merchant_name):
    # print("Transaction Data {}".format(transaction_data))
    
    match_flag = False
    
    if not pd.isnull(merchant_name):
        final_name = merchant_name.lower()
        # if merchant_name == "Sprint":
        #     print("merch vals {} + {} + {}".format(name,merchant_name,final_name))
        # if "Juan" in name:
        #     print("One")
        #     print(name, final_name)
        # return string.capwords(merchant_name)
    else:
        updated_name, match_flag = initial_merchant_check(name, merchant_name)
        # if name == "Sprint":
        #     print(name, updated_name)
        # if "Juan" in name:
        #     print("Two")
        #     print(name, updated_name)
    if match_flag == True:
        # final_name = string.capwords(updated_name)
        final_name = updated_name.lower()
        # if "Juan" in name:
        #     print("Three")
        #     print(name, updated_name)
    else:
        final_name = text_cleanup(name)
        # if "Juan" in name:
        #     print("Four")
        #     print(name, final_name)
    # print("Merchant Name {}".format(final_name))
    checked_name, status = final_merchant_check(final_name)
    if status == True:
        final_name = checked_name
        # if "Juan" in name:
        #     print("Five")
        #     print(name, final_name)
    # if name == "Sprint":
    #     print("Final vals {} + {} + {}".format(name,merchant_name,final_name))
    return string.capwords(final_name)


def final_merchant_check(name):
    ignore_keys = ["*","-","/","+",",","_", "&","(",":","@","|","."] 
    match=False
    name = name.lower()
        # print("NAME {}".format(name))
        # for ignore in ignore_keys:
        #     name = name.replace(ignore," ")
    name = name.split()
    resultwords = [word for word in name if word.lower() not in keywords_removal]
    name = ' '.join(resultwords)
    # print("NAME {}".format(name))
    # name_list = name.split()
    # print("NAME LIST {}".format(name_list))
    # keys_df = pd.DataFrame(merchant_list_map.keys())
    # keys_df.rename(columns={0:'keys'},inplace=True)
    # keys_df['strip_keys'] = keys_df['keys'].str.strip()
    # keys_df['match'] = keys_df.apply(lambda x: True if fuzz.token_set_ratio(x['strip_keys'],name) >= 90 else False,axis=1)
    # keys_df = keys_df[keys_df['match']==True]
    # if len(keys_df) == 0:
    #     return None,False
    # else:
    #     keys_df = keys_df.reset_index(drop=True)
    #     keys_df = keys_df.head(1)
    #     return merchant_list_map[keys_df['keys'][0]].lower(),keys_df['match'][0]


    for key, val in merchant_list_map.items():
        merchant_data = key.strip()
        # print(set(merchant_data.split()), name_list)
        # if "parkside" in name:
            # print(name)
            # print(fuzz.partial_token_ratio(merchant_data,name),key,merchant_list_map[key],name)
        if fuzz.token_set_ratio(merchant_data,name) >= 90:
            match = True
            return merchant_list_map[key], match
    return None, match