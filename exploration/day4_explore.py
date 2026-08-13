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

# Just the columns you need to document
target_cols = ['epa', 'wp', 'wpa', 'vegas_wp', 'down', 'ydstogo', 'yardline_100', 
               'game_seconds_remaining', 'score_differential', 
               'play_type', 'pass', 'rush', 'xpass', 'pass_oe', 'success', 
               'yards_gained']

pd.set_option('display.max_columns', None)  # Show all columns
#pd.set_option('display.width', None)  # Use full terminal width

# Show first 20 rows for these columns
print(pbp_pandas[target_cols].head(20))
