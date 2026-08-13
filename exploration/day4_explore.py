import nflreadpy as nfl
import pandas as pd
#imports

#loading in the play by play data
pbp = nfl.load_pbp([2023])
pbp_pandas = pbp.to_pandas()

"""
#look at first 5 rows
print(pbp_pandas.head(n=5)) #defaults to 5 with no input
print("\n" + "="*80+'\n')

#look at 1 row at a time (row 2 here)
print(pbp_pandas.iloc[1])
print("\n" + "="*80+'\n')

#look at columns and datatypes
print(pbp_pandas.info())
"""
#above outputs verified, now checking important stats
