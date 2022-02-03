import pandas as pd
import numpy as np
from configs.constants import *
from services.merchant_name_extractor import get_merchant_name
from services.utils import string_found
import logging
from configs.config import mode
import sys
import traceback

class INCOME_TYPE():

    def __init__(self,trans,min_line_date):
        self.trans = trans[trans['date']<=min_line_date].copy()
        # self.income_trans,self.expense_trans,self.trans = self.get_income_trans(self.trans)
        # self.income_trans = self.trans[self.trans['transactiontype']==2]
        self.income_trans = self.trans[self.trans['dsidentifiedas']=='income']
        # self.expense_trans = self.trans[self.trans['transactiontype']==0]
        self.expense_trans = self.trans[self.trans['dsidentifiedas']=='expense']

    def get_income_trans(self,df):
        logging.info("Started to tag Income....")
        if 'merchantname' not in df.columns:
            df['merchantname']  = np.nan
        if 'useridentifiedas' not in df.columns:
            df['useridentifiedas'] = np.nan
        df["merchantname"] = df.apply(lambda x: get_merchant_name(x["name"], x["merchantname"]), axis=1)

        logging.info("Income Tagging Comepleted using merchantName....")
        df['transType'] = df.apply(lambda x: 'Credit' if x['amount'] > 0 else 'Debit',axis=1)
        df['transactionCategory'] = np.nan
        df['transactionCategory'] = df.apply(lambda x: 'Loan' if x['name'].lower() in ('loan','loans') else x['transactionCategory'],axis=1)
        df["transactionCategory"] = df.apply(lambda x: self.income_transaction_type_check(x["transactionCategory"], x["name"], x["merchantname"], x["amount"],x["sourcecategories"]), axis=1)
        df["transactionCategory"] = df.apply(lambda x: 'Income' if (str(x['useridentifiedas']).lower()=='income' or str(x['markedasincome']).lower()=='true') else x["transactionCategory"],axis=1)

        df['probable_incomeFlag'] = df.apply(lambda x: 1 if x['transactionCategory'] == 'Income' and x['transType'] == 'Credit' else 0, axis=1)
        df['probable_expenseFlag'] = df.apply(lambda x: 1 if (x['transactionCategory'] == 'Non-Income' or x['transactionCategory'] == 'Loan') and x['transType'] == 'Debit' else 0, axis=1)

        income_trans = df[df['probable_incomeFlag']==1]
        expense_trans = df[df['probable_expenseFlag'] == 1]

        if mode == -1:
            income_trans = df[df['amount']>=0]
            expense_trans = df[df['amount']<0]

        logging.info("Income Tagging Comepleted....")
        return income_trans,expense_trans,df

    def income_transaction_type_check(self,transactionCategory, name, merchantName, amount, sourceCategories):
        # print("Transction Type {} {} {} {} {}".format(transactionType,name,merchantName,amount,sourceCategories))
        if amount > 0 and amount < 75:
            return "Non-Income"
        loan_list = [x.lower() for x in loan_products]
        filter_values = [x.lower() for x in filter_list]
        # total_income_transactions = []
        # inflow_data = transactions_data[transactions_data["amount"] >= 75].copy(deep=True)
        # print(loan_list)
        # print(filter_list)

        # if string_found("Benefits",sourceCategories):
        if "Benefits" in sourceCategories:
            # print("Benefits {}".format(transactionType))
            return "Non-Income"

        if "payroll" in name.lower() or ("deposit" in name.lower() and "direct" in name.lower()) or ("dep" in name.lower() and "direct" in name.lower()):
        # if string_found("payroll",name.lower()) or (string_found("deposit",name.lower()) and string_found("direct",name.lower())) or (string_found("dep",name.lower()) and string_found("direct", name.lower())):
            # print("Payroll {}".format(transactionType))
            return "Income"

        # if string_found("Payroll",sourceCategories) and not string_found("Benefits",sourceCategories):
        if "Payroll" in sourceCategories and "Benefits" not in sourceCategories:
            # print("Payroll {}".format(transactionType))
            return "Income"

        for loan in loan_list:
            if string_found(loan.lower(),merchantName.lower()) or string_found(loan.lower(),name.lower()):
            # if loan.lower() in merchantName.lower() or loan.lower() in name.lower():
                # print("Loans {}".format(transactionType))
                return "Non-Income"

        for value in filter_values:
            if string_found(value.lower(),merchantName.lower()) or string_found(value.lower(),name.lower()):
            # if value.lower() in merchantName.lower() or value.lower() in name.lower():
                # print("Values {}".format(transactionType))
                return "Non-Income"

        return transactionCategory





# print(string_found('nsf','MONEY TRANSFER AUTHORIZED ON 03/12 FROM Christina Lay CA S00380072392023071 CARD 4394'))