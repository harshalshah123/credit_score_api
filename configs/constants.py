new_cols = {'closing_bal':'Closing Balance',
'opening_bal':'Opening Balance',
'total_debit_amount':'Debits',
'total_no_of_debits':'Debit Counts',
'total_credit_amount':'Credits',
'total_no_of_credits':'Credit Counts',
'min_eod_balance':'Minimum Balance',
'max_eod_balance':'Maximum Balance',
'avg_eod_balance':'Average Balance'}

acct_cols=['sourceaccountid','deletestatus','mask','available','current','lastbalanceupdate','primary_acct_flag']

loan_products = ['ALBERT INSTANT',
'Brigit.com',
'CHECKCARD',
'Klover Holdings',
'KLOVER HOLDINGS',
'NSF',
'OVERDRAFT PROTECTION',
'OVERDRAFT',
'Earnin Active',
'Earnin',
'CLEO',
'Dave Inc ',
'Earnin-Activeh',
'FLOATME',
'MoneyLion',
'SILVER CLOUD FIN',
'TitleMax',
'CASH TIME TITLE LOANS',
'CASHTIME',
'CHECKCARD',
'CHECKMATE',
'SPEEDY CASH',
'DOLLAR FINANCIAL GROUP',
'FIRST LOAN',
'INBOX LOAN',
'INSTACASH PAYMENT',
'ML PLUS LOAN',
'MONEYLION',
'Makwa Finance',
'MoneyLion',
'EARNIN-ACTIVEHOURS',
'SPEEDY CASH',
'SPOTLOAN',
'VBS BigPicture ',
'VBS FirstLoan',
'VBS Inbox Loan',
'VBS Lendumo',
'VBS NatlSmlLoan',
'VBS_MAXLEND',
'BRANCH MESSENGER,',
'INSUFFICIENT FUNDS FEE',
'RETURNED ITEM FEE FOR AN UNPAID',
'ALBERT INSTANT',
'BRANCH MESSENGER INC ',
'Branch Messenger',
'FLOATME',
'Empower Inc',
'Pay Advance',
'Payadvance',
'Progressivelease',
'Betterday ',
'Pay Advance',
'Zebit Inc',
'ACE Cash Express',
'EarninActivehour',
'FLOATME',
'CHRYSLER CAPITAL PAYMENT',
'VBS Eagle Valley',
'VBS Rapid Title'
]

filter_list = ['venmo',
'chime',
'cash app',
'varo',
'save',
'spend',
'paypal',
'dave',
'zelle',
'brigit',
'robinhood',
'venmo',
'webull',
'stash',
'ameritrade',
'cashapp',
'fidelity',
'atm',
'klover'
]


primary_exp_categories = ['5e9972aa7cd42a3bfc5d3b6b','5e9972aa7cd42a3bfc5d3b6e','5e9972aa7cd42a3bfc5d3b76','5e9972aa7cd42a3bfc5d3b8c','5e9972aa7cd42a3bfc5d3b68','5e9972aa7cd42a3bfc5d3b70','5e9972aa7cd42a3bfc5d3b83','5e9972aa7cd42a3bfc5d3b8e','5e9972aa7cd42a3bfc5d3b79','5e9972aa7cd42a3bfc5d3b93','5e9972aa7cd42a3bfc5d3b7f','5e9972aa7cd42a3bfc5d3b6f','5e9972aa7cd42a3bfc5d3b6a','5e9972aa7cd42a3bfc5d3b90','5e9972aa7cd42a3bfc5d3b90','5e9972aa7cd42a3bfc5d3b75','5e9972aa7cd42a3bfc5d3b7e','5e9972aa7cd42a3bfc5d3b73','5e9972aa7cd42a3bfc5d3b86','5e9972aa7cd42a3bfc5d3b8b','5e9972aa7cd42a3bfc5d3b6d','5e9972aa7cd42a3bfc5d3b7b','5e9972aa7cd42a3bfc5d3b84','5e9972aa7cd42a3bfc5d3b74','5e9972aa7cd42a3bfc5d3b81','5e9972aa7cd42a3bfc5d3b87','5e9972aa7cd42a3bfc5d3b80','5e9972aa7cd42a3bfc5d3b89','5e9972aa7cd42a3bfc5d3b91','5e9972aa7cd42a3bfc5d3b72']
secondary_exp_categories = ['5e9972aa7cd42a3bfc5d3b8d','5e9972aa7cd42a3bfc5d3b82','5e9972aa7cd42a3bfc5d3b92','5e9972aa7cd42a3bfc5d3b6c','5e9972aa7cd42a3bfc5d3b8f','5e9972aa7cd42a3bfc5d3b78','5e9972aa7cd42a3bfc5d3b7c','5e9972aa7cd42a3bfc5d3b88','5e9972aa7cd42a3bfc5d3b77','5e9972aa7cd42a3bfc5d3b71','5e9972aa7cd42a3bfc5d3b7a','5e9972aa7cd42a3bfc5d3b85']

primary_master_cols = ['B0M00 Closing Balance','B0M01 Closing Balance','B0M02 Closing Balance','B0M03 Closing Balance','B0M04 Closing Balance','B0M05 Closing Balance','B0M06 Closing Balance','B0M07 Closing Balance','B0M08 Closing Balance','B0M09 Closing Balance','B0M10 Closing Balance','B0M11 Closing Balance','B0M00 Opening Balance','B0M01 Opening Balance','B0M02 Opening Balance','B0M03 Opening Balance','B0M04 Opening Balance','B0M05 Opening Balance','B0M06 Opening Balance','B0M07 Opening Balance','B0M08 Opening Balance','B0M09 Opening Balance','B0M10 Opening Balance','B0M11 Opening Balance','B0M00 Credits','B0M01 Credits','B0M02 Credits','B0M03 Credits','B0M04 Credits','B0M05 Credits','B0M06 Credits','B0M07 Credits','B0M08 Credits','B0M09 Credits','B0M10 Credits','B0M11 Credits','B0M00 Debits','B0M01 Debits','B0M02 Debits','B0M03 Debits','B0M04 Debits','B0M05 Debits','B0M06 Debits','B0M07 Debits','B0M08 Debits','B0M09 Debits','B0M10 Debits','B0M11 Debits','B0M00 Credit Counts','B0M01 Credit Counts','B0M02 Credit Counts','B0M03 Credit Counts','B0M04 Credit Counts','B0M05 Credit Counts','B0M06 Credit Counts','B0M07 Credit Counts','B0M08 Credit Counts','B0M09 Credit Counts','B0M10 Credit Counts','B0M11 Credit Counts','B0M00 Debit Counts','B0M01 Debit Counts','B0M02 Debit Counts','B0M03 Debit Counts','B0M04 Debit Counts','B0M05 Debit Counts','B0M06 Debit Counts','B0M07 Debit Counts','B0M08 Debit Counts','B0M09 Debit Counts','B0M10 Debit Counts','B0M11 Debit Counts','B0M00 Maximum Balance','B0M01 Maximum Balance','B0M02 Maximum Balance','B0M03 Maximum Balance','B0M04 Maximum Balance','B0M05 Maximum Balance','B0M06 Maximum Balance','B0M07 Maximum Balance','B0M08 Maximum Balance','B0M09 Maximum Balance','B0M10 Maximum Balance','B0M11 Maximum Balance','B0M00 Minimum Balance','B0M01 Minimum Balance','B0M02 Minimum Balance','B0M03 Minimum Balance','B0M04 Minimum Balance','B0M05 Minimum Balance','B0M06 Minimum Balance','B0M07 Minimum Balance','B0M08 Minimum Balance','B0M09 Minimum Balance','B0M10 Minimum Balance','B0M11 Minimum Balance','B0M00 Average Balance','B0M01 Average Balance','B0M02 Average Balance','B0M03 Average Balance','B0M04 Average Balance','B0M05 Average Balance','B0M06 Average Balance','B0M07 Average Balance','B0M08 Average Balance','B0M09 Average Balance','B0M10 Average Balance','B0M11 Average Balance']
cum_master_cols = ['C1M00 month_year','C1M01 month_year','C1M02 month_year','C1M03 month_year','C1M04 month_year','C1M05 month_year','C1M06 month_year','C1M07 month_year','C1M08 month_year','C1M09 month_year','C1M10 month_year','C1M11 month_year','C1M00 Closing Balance','C1M01 Closing Balance','C1M02 Closing Balance','C1M03 Closing Balance','C1M04 Closing Balance','C1M05 Closing Balance','C1M06 Closing Balance','C1M07 Closing Balance','C1M08 Closing Balance','C1M09 Closing Balance','C1M10 Closing Balance','C1M11 Closing Balance','C1M00 Opening Balance','C1M01 Opening Balance','C1M02 Opening Balance','C1M03 Opening Balance','C1M04 Opening Balance','C1M05 Opening Balance','C1M06 Opening Balance','C1M07 Opening Balance','C1M08 Opening Balance','C1M09 Opening Balance','C1M10 Opening Balance','C1M11 Opening Balance','C1M00 Credits','C1M01 Credits','C1M02 Credits','C1M03 Credits','C1M04 Credits','C1M05 Credits','C1M06 Credits','C1M07 Credits','C1M08 Credits','C1M09 Credits','C1M10 Credits','C1M11 Credits','C1M00 Debits','C1M01 Debits','C1M02 Debits','C1M03 Debits','C1M04 Debits','C1M05 Debits','C1M06 Debits','C1M07 Debits','C1M08 Debits','C1M09 Debits','C1M10 Debits','C1M11 Debits','C1M00 Credit Counts','C1M01 Credit Counts','C1M02 Credit Counts','C1M03 Credit Counts','C1M04 Credit Counts','C1M05 Credit Counts','C1M06 Credit Counts','C1M07 Credit Counts','C1M08 Credit Counts','C1M09 Credit Counts','C1M10 Credit Counts','C1M11 Credit Counts','C1M00 Debit Counts','C1M01 Debit Counts','C1M02 Debit Counts','C1M03 Debit Counts','C1M04 Debit Counts','C1M05 Debit Counts','C1M06 Debit Counts','C1M07 Debit Counts','C1M08 Debit Counts','C1M09 Debit Counts','C1M10 Debit Counts','C1M11 Debit Counts','C1M00 Maximum Balance','C1M01 Maximum Balance','C1M02 Maximum Balance','C1M03 Maximum Balance','C1M04 Maximum Balance','C1M05 Maximum Balance','C1M06 Maximum Balance','C1M07 Maximum Balance','C1M08 Maximum Balance','C1M09 Maximum Balance','C1M10 Maximum Balance','C1M11 Maximum Balance','C1M00 Minimum Balance','C1M01 Minimum Balance','C1M02 Minimum Balance','C1M03 Minimum Balance','C1M04 Minimum Balance','C1M05 Minimum Balance','C1M06 Minimum Balance','C1M07 Minimum Balance','C1M08 Minimum Balance','C1M09 Minimum Balance','C1M10 Minimum Balance','C1M11 Minimum Balance','C1M00 Average Balance','C1M01 Average Balance','C1M02 Average Balance','C1M03 Average Balance','C1M04 Average Balance','C1M05 Average Balance','C1M06 Average Balance','C1M07 Average Balance','C1M08 Average Balance','C1M09 Average Balance','C1M10 Average Balance','C1M11 Average Balance']

predictors = ['no_of_unique_lenders_1m','avg_debt_amt_1m','C1M00 Debit Counts','liquidity','avg_debt_amt_3m','currentObligationsValue','C1M00 secondary exp','C1M00 Closing Balance','C1_COV_DBC','C1M01 Debit Counts']
response_cols = ['userid','no_of_unique_lenders_1m','avg_debt_amt_1m','C1M00 Debit Counts','liquidity','avg_debt_amt_3m','currentObligationsValue','C1M00 secondary exp','C1M00 Closing Balance','C1_COV_DBC','C1M01 Debit Counts','primaryLenders_avg_debt_amt_1m','monthlyExp','weeklyExp']
score_cols = ['score','scoreBin','qualified_plan','micro_qualified_amt','medium_qualified_amt']
other_cols = ['C1M00 Closing Balance','C1M01 Closing Balance','C1M02 Closing Balance','C1M03 Closing Balance','C1M04 Closing Balance','C1M05 Closing Balance','C1M06 Closing Balance','C1M07 Closing Balance','C1M08 Closing Balance','C1M09 Closing Balance','C1M10 Closing Balance','C1M11 Closing Balance','C1M00 Opening Balance','C1M01 Opening Balance','C1M02 Opening Balance','C1M03 Opening Balance','C1M04 Opening Balance','C1M05 Opening Balance','C1M06 Opening Balance','C1M07 Opening Balance','C1M08 Opening Balance','C1M09 Opening Balance','C1M10 Opening Balance','C1M11 Opening Balance','C1M00 Debits','C1M01 Debits','C1M02 Debits','C1M03 Debits','C1M04 Debits','C1M05 Debits','C1M06 Debits','C1M07 Debits','C1M08 Debits','C1M09 Debits','C1M10 Debits','C1M11 Debits','C1M00 Debit Counts','C1M01 Debit Counts','C1M02 Debit Counts','C1M03 Debit Counts','C1M04 Debit Counts','C1M05 Debit Counts','C1M06 Debit Counts','C1M07 Debit Counts','C1M08 Debit Counts','C1M09 Debit Counts','C1M10 Debit Counts','C1M11 Debit Counts','C1M00 Credits','C1M01 Credits','C1M02 Credits','C1M03 Credits','C1M04 Credits','C1M05 Credits','C1M06 Credits','C1M07 Credits','C1M08 Credits','C1M09 Credits','C1M10 Credits','C1M11 Credits','C1M00 Credit Counts','C1M01 Credit Counts','C1M02 Credit Counts','C1M03 Credit Counts','C1M04 Credit Counts','C1M05 Credit Counts','C1M06 Credit Counts','C1M07 Credit Counts','C1M08 Credit Counts','C1M09 Credit Counts','C1M10 Credit Counts','C1M11 Credit Counts','C1M00 Minimum Balance','C1M01 Minimum Balance','C1M02 Minimum Balance','C1M03 Minimum Balance','C1M04 Minimum Balance','C1M05 Minimum Balance','C1M06 Minimum Balance','C1M07 Minimum Balance','C1M08 Minimum Balance','C1M09 Minimum Balance','C1M10 Minimum Balance','C1M11 Minimum Balance','C1M00 Maximum Balance','C1M01 Maximum Balance','C1M02 Maximum Balance','C1M03 Maximum Balance','C1M04 Maximum Balance','C1M05 Maximum Balance','C1M06 Maximum Balance','C1M07 Maximum Balance','C1M08 Maximum Balance','C1M09 Maximum Balance','C1M10 Maximum Balance','C1M11 Maximum Balance','C1M00 Average Balance','C1M01 Average Balance','C1M02 Average Balance','C1M03 Average Balance','C1M04 Average Balance','C1M05 Average Balance','C1M06 Average Balance','C1M07 Average Balance','C1M08 Average Balance','C1M09 Average Balance','C1M10 Average Balance','C1M11 Average Balance','C1_COV_DBC','C1M00 income','C1M01 income','C1M02 income','C1M03 income','C1M04 income','C1M05 income','C1M06 income','C1M07 income','C1M08 income','C1M09 income','C1M10 income','C1M11 income','no_of_unique_lenders_1m','no_of_unique_lenders_3m','primaryLenders_avg_debt_amt_3m','primaryLenders_avg_debt_amt_1m','primaryLenders_total_debt_amt_3m','primaryLenders_total_debt_amt_1m','C1M00 expense','C1M01 expense','C1M02 expense','C1M03 expense','C1M04 expense','C1M05 expense','C1M06 expense','C1M07 expense','C1M08 expense','C1M09 expense','C1M10 expense','C1M11 expense','monthlyIncome','weeklyIncome','monthlyExp','weeklyExp']

approved_bins = [0,1,2,3,4,5]