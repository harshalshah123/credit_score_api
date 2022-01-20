import pandas as pd
import numpy as np


def check_transaction_timeperiod(num_months):

    if num_months >= 6:
        return True
    else:
        return False

