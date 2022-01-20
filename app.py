import datetime
import os
import logging
import json #, ast
import numpy as np
import pandas as pd
import pickle
from configs.config import LOGGER_PATH as lp,MODEL_PATH,ip_address
from configs.constants import response_cols,predictors,score_cols,other_cols
from flask import Flask, request, jsonify
from main_app.run_app import CREDIT_SCORE
import warnings
warnings.filterwarnings('ignore')

app = Flask(__name__)
print(ip_address)
app_start_date = datetime.datetime.now()
logging.basicConfig(filename=os.path.join(lp, 'pre_log_' + str(app_start_date.strftime('%d-%m-%Y_%H%M%S')) + '.log'), level=logging.INFO, format="%(asctime)s :: %(message)s", datefmt="%d-%m-%Y_%H:%M:%S")
woe_bins = pd.read_csv(MODEL_PATH+"woe.csv")
loaded_model = pickle.load(open(MODEL_PATH+"logi_model_final.pkl", 'rb'))

@app.route('/')
def welcome():
    return "Welcome to the Prediction."
    # return distribution_json

@app.route('/get_creditscore', methods=['GET', 'POST'])
def add_message():
    start_time = datetime.datetime.now()
    if request.method == 'POST':

        content = json.loads(request.data)
        logging.info("Request Data :: %s ", str(content))
        data = content['data'] if 'data' in content.keys() else pd.DataFrame()

        data_df = pd.DataFrame.from_dict(data,orient='index').T
        data_df.replace("nan", np.nan, inplace=True)

    elif request.method == 'GET':
        data_df = pd.DataFrame.from_dict(request.values.dicts[0], orient='index').T
        data_df.replace("nan", np.nan, inplace=True)
        print(data_df)

        # insert_data(raw_data, start_time)
    # api_response_df = pd.DataFrame()
    # api_response_df['userid'] = data_df.copy(deep=True)

    if len(data_df) == 1:
        data_df['created_date'] = start_time
        sim = CREDIT_SCORE(data_df,woe_bins,loaded_model)
        if sim.model_score_flag:
            # scored_df = sim.final_df[response_cols]
            # scored_df['DS_CALCULATED_FLAG'] = sim.model_score_flag
            # scored_df['created_date'] = start_time
            features = sim.final_df[predictors].to_dict('records')
            transformed = sim.transformed_df[predictors].to_dict('records')
            scores = sim.final_df[score_cols].to_dict('records')
            try:
                other_para = sim.final_df[other_cols].to_dict('records')
            except:
                other_para = []
            data_df['model_score_flag'] = sim.model_score_flag
            userinfo = data_df.to_dict('records')

            # a[0]['payment_dates'] = sim.incomeobj.income_prediction_dates
            d = {"data":{"userid":userinfo,"features": features,'transformed_data':transformed,'qualification':scores,'otherParameters':other_para}}
            logging.info("Scoring Response.. ==:: %s ", str(d))
        else:
            error_df = data_df[['userid']].copy()
            error_df['errorMsg'] = sim.error_message
            error_df['created_date'] = start_time
            error_df['DS_CALCULATED_FLAG'] = sim.model_score_flag
            d = {"data": error_df.to_dict('records')}
            logging.info("Scoring Response.. ==:: %s ", str(d))

    else:
        if len(data_df) == 0:
            d = {"DS_CALCULATED_FLAG": False,"errorMsg": "No Data","created_date": start_time}
        else:
            d = {"DS_CALCULATED_FLAG": False,"errorMsg": "More than one userids in request","created_date": start_time}

    return jsonify(d)


if __name__ == '__main__':
    app.run(host=ip_address, port=9003, threaded=True)
