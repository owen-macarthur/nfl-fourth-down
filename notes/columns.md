# EPA
## Expected points added
The amount of points the given play is expected to add to a teams score.
Presnap: an EP (Expected Points) is calculated. It represents how many points an offense is statistically expected to score on that drive. It factors in down, distance, field position, time remaining, etc to calculate it

Post-Play: Calculates a new EP value

EPA = EP after play - EP before play

# WP
## Win Probability
Estimated likliness for the team with possesion to win the game at the START of the given play

# WPA
## win Probability Added
Similar to epa, it subtracts the WP from before the play from the WP after the play

# VEGAS_WP
## Vegas Win Probability
WP, but it factors in the pre-game vegas spread.

# DOWN
The down for the given play. (1st, 2nd, 3rd, or 4th)

# YDSTOGO
## Yards to go
The distance in yards to the first down marker (or the endzone in __ & goal situations)

# YARDLINE_100
Yards from opponents endzone

# GAME_SECONDS_REMAINING
Number of seconds remaining in the entire game

# SCORE_DIFFERENTIAL
How many points the team with posession is winning by before the snap (pos means they are winning, neg means they losing)

# POSTEAM_TIMEOUTS_REMAINING
Number of timeouts remaining for team with possession

# PLAY_TYPE
## Type of play being ran, shown below (note: rpos and 2pt conversions count as whichever type happened(run or pass)):
pass- Pass attempts(completions, incompletions, interceptions) and sacks (including strip sacks)
run- Designed runs and QB Scrambles 
no_play- penalties that wipe out a down, team/booth timeouts, aborted snaps
        aborted snap is a snap that is not cleanly controlled and a player just jumps on it
        wiping out a down is the following penalty types: pre-snap, post snap that result in replay (holding, pi, block in the back), offsetting penalties
punt- all punt attempts (whether blocked or returned), including punts after a safety
kickoff- opening, second half, or post score 
field_goal- field goal attempt (whether made, missed, or blocked)
extra_point- PAT kick attempt
qb_kneel
qb_spike
NA- End of quarter, 2 minute warning, or game over where game is paused

# PASS
BINARY indicator on if a play was a pass play (sacks, scrambles, and plays with penalties included)

# RUSH
BINARY indicator on if a play was a run play

# TWO_POINT_ATTEMPT
BINARY indicator on if a play was a 2 point conversion

# QB_DROPBACK
BINARY indicator on whether or not a qb dropped back on the play (includes all pass attempts, sacks, or scrambles)

# SHOTGUN
BINARY indicator on if a play was run out of the shotgun

# NO_HUDDLE
BINARY indicator on if a play was run after no huddle occured

# XPASS
## Expected Pass Frequency
Based off of historical NFL data, what is the probability a team passes the ball in this exact game situation

# PASS_OE
## Pass Rate Over Expected
Dropback percentage over expected dropback percentage scaled from -100 to 100

# FOURTH_DOWN_CONVERTED
BINARY indicator on if a first down was converted on a 4th down situation

# FOURTH_DOWN_FAILED
BINARY indicator on if a first down was not converted on a 4th down situation

# SUCCESS
BINARY indicator on if EPA was possitive on a given play

# YARDS_GAINED
Total Yards gained or lost on the given play before fumbles, laterals, or ints