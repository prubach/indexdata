from numpy import *
import numpy as np
import pandas as pd
from util.findata import FinData
import os

DATA_DIR = os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', 'data')
os.makedirs(DATA_DIR, exist_ok=True)

def download_indices_for_period(indices, start_date=None, end_date=None, years=None):
    if start_date is None or end_date is None:
        start_date = str(years[0]) + '-01-01'
        end_date = str(years[1]) + '-12-31'
    fin = FinData(start_date, end_date, 'stooq', 'Close')
    # setup dataframe matrix
    df = pd.DataFrame([
        fin.ind(idx) for idx in indices
    ]).T
    # drop rows with empty values (holidays)
    df = df.dropna()
    # log of the absolute value of the return rate :
    # x(t)=log(y(t)) - log(y(t-1))
    #print(len(df))
    # df = np.log(df) - np.log(df.diff(periods=1))
    # normalize data
    # df=(df-df.mean())/df.std()
    # df = df/df.max().astype(np.float64)
    # df=(df-df.min())/(df.max()-df.min())
    #print(df.head())
    #print(df.tail())
    # print(df)
    # source matrix as transposed dataframe data
    if len(years) > 0:
        file_name = get_file_name(indices, years)
    else:
        ind_str = "_".join(indices).replace('^', '')
        file_name = os.path.join(DATA_DIR, 'sources_' + ind_str + '.csv')
    df.to_csv(file_name, index=True, header=True)


def get_file_name(indices, years):
    ind_str = "_".join(indices).replace('^', '')
    str_years = "_".join(['{0}'.format(y) for y in years])
    return os.path.join(DATA_DIR, 'sources_' + ind_str + '__' + str_years + '.csv')


def read_data(indices, years=[2000, 2020], log_ret=True):
    file_name = get_file_name(indices, years)
    if not os.path.exists(file_name) or os.path.getsize(file_name) < 50:
        download_indices_for_period(indices, years=years)
    df = pd.read_csv(file_name, header=0, index_col=0)
    # logarytmiczne stopy zwrotu
    if log_ret:
        df = np.log(df) - np.log(df.shift(-1))
        df = df.dropna()
    return df

