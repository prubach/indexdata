from util.stooq_download import read_data

indices = ['^SPX', '^DJC', '^DAX', '^NDX', 'WIG20']
df = read_data(indices,  years=[2005, 2019], log_ret=True)
print(df)