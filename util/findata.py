import pandas as pd
import pandas_datareader.data as web

class FinData(object):
    def __init__(self, start_date, end_date, source = 'stooq', column = 'Close'):
        self.start_date = start_date
        self.end_date = end_date
        self.source = source
        self.column = column

    def get_all(self, name):
        filtered_name = name[1:] if name.startswith('^') else name
        #try:
        #    ind_all = pd.read_csv('data/' + name.lower() + "_" + str(self.start_date) + "_" + str(self.end_date) + "_d.csv")
        #except OSError:
        ind_all = web.DataReader(name, self.source, start=self.start_date, end=self.end_date)
        ind_all.rename(columns={self.column: filtered_name}, inplace=True)
        return ind_all[filtered_name]

    def ind(self, name):
        df = self.get_all(name)
        # mask = (df.index > self.start_date) & (df.index <= self.end_date)
        # return df.loc[mask]
        return df