import re
from configs.merchant_list import merchant_list_map,keywords_removal
import pandas as pd

def initial_merchant_check(name,merchant_name=None):
    ignore_keys = ["*","-","/","+",",","_", "&","(",":","@","|","."] 
    match = False
    if not pd.isnull(merchant_name):
        return merchant_name
    else:
        name = name.lower()
        # print("NAME {}".format(name))
        # for ignore in ignore_keys:
        #     name = name.replace(ignore," ")
        name = name.split()
        resultwords = [word for word in name if word.lower() not in keywords_removal]
        name = ' '.join(resultwords)
    # print("NAME {}".format(name))
    name_list = name.split()

    # keys_df = pd.DataFrame(merchant_list_map.keys())
    # keys_df.rename(columns={0:'keys'},inplace=True)
    # keys_df['strip_keys'] = keys_df['keys'].str.strip()
    # keys_df['match'] = keys_df.apply(lambda x: True if set(x['strip_keys'].split()).issubset(name_list) else False,axis=1)
    # keys_df = keys_df[keys_df['match']==True]
    # if len(keys_df) == 0:
    #     return None,False
    # else:
    #     keys_df = keys_df.reset_index(drop=True)
    #     keys_df = keys_df.head(1)
    #     return merchant_list_map[keys_df['keys'][0]].lower(),keys_df['match'][0]
    # print("NAME LIST {}".format(name_list))
    for key, val in merchant_list_map.items():
        merchant_data = key.strip()
        # print(set(merchant_data.split()), name_list)

        if set(merchant_data.split()).issubset(name_list):
            match = True
            return merchant_list_map[key].lower(), match
    return None, match


def text_cleanup(text):
    
    ###Lower casing everything
    text = text.lower()
    ignore_keys = ["*","-","/","+",",","_", "&","(",":","@","|","."]
    for ignore in ignore_keys:
        text = text.replace(ignore," ")
    #     print(text)
    filter_list = ["*","#",",",":"]
    # for i in range(len(x)):
    #     print(x[i])
    #     if x[i] in filter_list:
    #         print(x[i])
    ###Filtering for keywords
    text = remove("xxx", text)
    try:
        n = min([i for i in range(len(text)) if text[i] in filter_list])
        text = text[:n]
    except:
        pass
    ###Filtering for dates (mm/dd)   
    try:
        d = min([x.start(0) for x in re.finditer(r'\d{2}/\d{2}',text)])
        text = text[:d]
    except:
        pass
    ###Filtering for transaction ids and beyond
    try:
        t = min([x.start(0) for x in re.finditer(r'\d{6,}',text)])
        # print(t)
        text = text[:t]
    except:
        pass

    name = text.split()
    resultwords = [word for word in name if word.lower() not in keywords_removal]
    name = ' '.join(resultwords)

    return text.strip().lower()


def remove(rem,my_string):
    return re.sub(".*"+rem+".*\n?","",my_string)
