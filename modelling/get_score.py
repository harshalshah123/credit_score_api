import pandas as pd
from services.utils import woe_transformation
from configs.constants import predictors
import logging
def run_model(df,woe_bins,loaded_model):
    logging.info("Model started...")
    new_bin_cuts = [0, 537, 553, 569, 584, 600, 615, 630, 645,660,1000]


    transformed_df = woe_transformation(df[predictors],woe_bins,True)
    transformed_df['pred'] = loaded_model.predict_proba(transformed_df[predictors])[:, 1]
    transformed_df['score'] = transformed_df.apply(lambda x: round((float(x['pred'])*(-211.90))+709.78,0),axis=1)
    transformed_df['score'] = transformed_df['score'].apply(lambda x: 300 if x < 300 else 900 if x >900 else x)
    transformed_df['scoreBin'] = pd.cut(transformed_df['score'], bins=new_bin_cuts,labels=[10, 9, 8, 7, 6, 5, 4, 3, 2, 1])
    transformed_df = transformed_df.join(df[['userid']])
    return transformed_df