import nflreadpy as nfl
pbp = nfl.load_pbp([2023])
print(pbp.shape)
print(pbp.columns)