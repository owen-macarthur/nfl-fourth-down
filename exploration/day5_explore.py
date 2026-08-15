import nflreadpy as nfl
import pandas as pd
#imports

#loading in the play by play data
pbp = nfl.load_pbp([2023])
pbp_pd = pbp.to_pandas()

# Creating Series and DataFrame practice
# 1. Create a Series from a single column (pass or down)
series1 = pd.Series(pbp_pd["pass"])
#print(series1.head(n=10))

# 2. Create a DataFrame by selecting 3–4 columns
df2 = pd.DataFrame(pbp_pd[['pass', 'epa', 'wpa']])
#print(df2.head(n=10))

# 3. Create a Series with a custom string index (team names or play types)
#series3 = pd.Series(pbp_pd['play_type'], index=pbp_pd['posteam'])
#print(series3.head(n=10))
#print(pbp_pd[['posteam','play_type']].head(n=10))
#print(pbp_pd['play_type'].head(n=10))
#print(pbp_pd['posteam'].head(n=10))


#print(pbp_pd['play_type'].values[:10])
#print(pbp_pd['posteam'].values[:10])
series3 = pd.Series(pbp_pd['play_type'].values, index=pbp_pd['posteam'].values)
#print(series3.head(n=10))

# Wow. there something weird when pyarrow converts polars to pandas. it weirds out about the columns sometimes and writes everything as NaN, so .values helps keep everything forced. not always needed, but good practice to include

# 4. Create a DataFrame from scratch using a dict (doesn't need to be NFL data; make up toy data)
#dictionary is the colon things
df4 = pd.DataFrame(
    {
        'Team': ['Giants', 'Cowboys', 'Eagles', 'Commanders'],
        'QB': ["Jaxson Dart", 'Dak Prescott', "Jalen Hurts", "Jayden Daniels"],
        'Wr1': ["Malik Nabers", "CeeDee Lamb", "DeVonta Smith", 'Terry McLaurin'],
    }
)
#print(df4)


#Getitem practice
# 1. Pull epa as a Series and print its length.
epa_series = pbp_pd['epa']

# 2. Pull down, ydstogo, and yardline_100 as a DataFrame. Confirm the shape.
down_ydstogo_yardline_100_df = pbp_pd[['down', 'ydstogo', 'yardline_100']]
# 3. Print rows 100–110 (all columns), then print those same rows with only the three columns from #2.
df100_to_110 = pbp_pd[100:110]
df_2_and_3 = df100_to_110[['down', 'ydstogo', 'yardline_100']]

print('1. Pull epa as a Series and print its length')
print(len(epa_series))
print('\n' + '='*80 + '\n')
print('2. Pull down, ydstogo, and yardline_100 as a DataFrame. Confirm the shape')
print(down_ydstogo_yardline_100_df.shape)
print('\n' + '='*80 + '\n')
print('3. Print rows 100–110 (all columns), then print those same rows with only the three columns from #2')
print(df100_to_110)
print('-'*80)
print(df_2_and_3)
