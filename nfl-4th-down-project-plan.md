# NFL Predictability & 4th Down Decision Model — 6 Week Plan

**Target:** ~1 hour/day, 42 days. Day 7 of each week is a buffer — use it to catch up, or to rest if you're ahead. Falling a day or two behind is normal and expected; don't compress the buffer days out of guilt.

**Core research question:** Does being predictable cost an offense? And can a 4th down decision model do better by accounting for it?

**Rule for the whole project:** when you're stuck, ask for an *explanation* or a *code review*, not for the code. You'll forget anything I write for you within a week.

---

## Week 1 — Environment, Git, and getting your hands on the data

### Day 1 — Python project setup
**Goal:** a clean, isolated project folder that won't fight you later.

- Make a folder `nfl-fourth-down/`
- Create a virtual environment: `python -m venv .venv`, then activate it
- `pip install nflreadpy pandas numpy matplotlib scikit-learn`
- `pip freeze > requirements.txt`
- Write a 3-line `test.py` that imports everything and prints "ok"

**Learn:** what a virtual environment actually *is* and why global pip installs cause pain.
**Resource:** Real Python's "Python Virtual Environments: A Primer" (realpython.com). Read the first third; skip the advanced sections.

### Day 2 — Git from the command line
**Goal:** stop using GitHub Desktop for this project.

You already know Desktop, which means you know the concepts. Today is about the commands, because in an interview "I use the GUI" reads differently than "I rebased a branch."

- Play through **Learn Git Branching** (learngitbranching.js.org) — the "Introduction Sequence" only, ~30 min. It's interactive and genuinely the best thing out there.
- Then in your project: `git init`, make a `.gitignore` (add `.venv/`, `__pycache__/`, `data/`, `*.parquet`), `git add`, `git commit`, create the repo on GitHub, `git remote add origin`, `git push`

**Key idea to actually understand:** the difference between working directory → staging area → commit. That's the thing GUIs hide from you.

### Day 3 — First contact with the data
**Goal:** pull play-by-play data and see what you're working with.

```python
import nflreadpy as nfl
pbp = nfl.load_pbp([2023])
print(pbp.shape)
print(pbp.columns)
```

Remember: this is a **Polars** DataFrame. Convert with `.to_pandas()` and work in pandas for now — there's far more help available online for pandas, and you don't need Polars' speed at this scale.

**Learn:** browse the nflreadpy docs (nflreadpy.nflverse.com) to see what other `load_*` functions exist. You'll want `load_schedules()` later.

### Day 4 — The data dictionary
**Goal:** this is the highest-value hour of week 1. Do not skip it.

The pbp table has ~370 columns. Open the nflfastR field descriptions page (nflfastr.com — look for "Field Descriptions" under Articles) and read through it with your `pbp` dataframe open next to it.

Make a text file `notes/columns.md` and write down, in your own words, what these mean: `epa`, `wp`, `wpa`, `vegas_wp`, `down`, `ydstogo`, `yardline_100`, `game_seconds_remaining`, `score_differential`, `posteam_timeouts_remaining`, `play_type`, `pass`, `rush`, `qb_dropback`, `shotgun`, `no_huddle`, `xpass`, `pass_oe`, `fourth_down_converted`, `fourth_down_failed`, `success`, `yards_gained`.

**Why this matters:** every leakage bug you'll ever have starts with not knowing what a column means.

### Day 5 — pandas fundamentals
**Goal:** filter, select, group, aggregate without googling every line.

- Read "10 minutes to pandas" in the official docs (pandas.pydata.org/docs/user_guide/10min.html) — it takes more than 10 minutes, budget the full hour
- Focus specifically on: boolean masking, `.loc`, `.groupby().agg()`, `.value_counts()`, `.merge()`

**Practice on real data:** how many plays per season? What's the distribution of `play_type`? How many 4th down plays are there per season?

### Day 6 — Reproduce a known number
**Goal:** prove to yourself that you understand the data, by computing something you can check against reality.

Compute **EPA per play on offense, by team, for 2023.** Filter to plays where `pass == 1 or rush == 1`, group by `posteam`, take the mean of `epa`, sort descending.

Then google "2023 NFL offensive EPA per play" and check your top 5 against a public leaderboard. If they don't match, figure out why before moving on — usually it's a filtering issue (penalties, kneels, spikes, two-point conversions).

**This is a real skill:** validating your pipeline against a known ground truth before you build anything on top of it.

### Day 7 — Buffer + README
Catch up on anything unfinished. Then write a first `README.md` describing what the project will be. Commit and push. Even a rough README makes the repo look intentional from day one.

---

## Week 2 — Pipeline and features

### Day 8 — The pre-snap audit
**Goal:** build your leakage defense before you build any model.

Go through your column notes and sort every column you care about into three buckets in `notes/columns.md`:

1. **Pre-snap** — a coach could know this before calling the play
2. **Post-snap** — describes what happened (labels, or forbidden features)
3. **Derived/model output** — `epa`, `wp`, `xpass`, `pass_oe` are outputs of other people's models

Bucket 3 is subtle: `wp` is fine as a *feature* (it's computed from pre-snap state), but `wpa` is not (it's the change caused by the play).

### Day 9 — The feature whitelist module
Write `src/features.py` containing an explicit list:

```python
PRESNAP_FEATURES = [
    "down", "ydstogo", "yardline_100", "score_differential",
    "game_seconds_remaining", "half_seconds_remaining",
    "posteam_timeouts_remaining", "defteam_timeouts_remaining",
    "qtr", "wp", "spread_line", "total_line",
]
```

Plus a function `build_playcall_dataset(pbp)` that filters to run/pass plays and returns `X` (whitelist columns only) and `y` (`pass`).

**Deliberately leave out `shotgun` and `no_huddle`** for now — we discussed why. Add a flag so you can toggle them later.

### Day 10 — Filtering, carefully
**Goal:** decide what counts as a play.

Exclude: kneels (`qb_kneel`), spikes (`qb_spike`), plays with no `down` (kickoffs, PATs), two-point conversions, and plays wiped out by penalty where no play happened. Handle missing values explicitly rather than letting pandas silently drop rows.

Print your row count before and after each filter. Write the counts in your notes.

### Day 11 — Caching your data
**Goal:** stop re-downloading 20 seasons every time you run a script.

Write `src/data.py` with a function that loads seasons 2016–2024, applies your filters, and saves the result to `data/plays.parquet`. If the file exists, load it instead of downloading.

**Learn:** what Parquet is and why it beats CSV for this (typed columns, compression, much faster reads).

### Day 12 — matplotlib basics
**Goal:** make charts that don't look like defaults.

- Work through the official pyplot tutorial (matplotlib.org)
- Learn the difference between the `plt.plot()` style and the `fig, ax = plt.subplots()` style. **Use the second one.** It's what you'll need for anything with subplots.
- Learn: axis labels, titles, `figsize`, saving to PNG at a sensible DPI

### Day 13 — Exploratory charts
Make three real charts and save them to `figures/`:

1. Pass rate by down and distance bucket (heatmap or grouped bars)
2. Pass rate by score differential and time remaining
3. Team pass rate over expected for 2024, using the built-in `pass_oe` column — this shows you what the answer *should* roughly look like before you build your own model

### Day 14 — Buffer + commit
Push everything. Write a short entry in `notes/log.md` describing what you learned this week. You'll be glad to have this when writing the final report.

---

## Week 3 — Your first model, and how to know if it's any good

### Day 15 — Logistic regression, conceptually
**Goal:** understand the model before you call the function.

- Watch StatQuest's "Logistic Regression" series on YouTube (Josh Starmer). The main video plus "Logistic Regression Details Pt 1" is about right for an hour.
- Key ideas: log-odds, the sigmoid, why the output is a *probability* and not a class

**Why start here and not XGBoost:** a linear baseline tells you how much of the signal is trivially learnable. If XGBoost only beats logistic regression by 0.5%, the fancy model isn't earning its complexity.

### Day 16 — Train the baseline
Write `src/train_playcall.py`. Use `sklearn.linear_model.LogisticRegression` on your whitelist features, train on 2016–2022.

Two things that will bite you:
- Scale your numeric features (`StandardScaler`) or the solver will complain and converge badly
- Use `predict_proba()`, not `predict()`. You want probabilities.

### Day 17 — Evaluation metrics that actually matter
**Goal:** understand why accuracy is the wrong metric here.

- **Log loss** — punishes confident wrong answers harshly
- **Brier score** — mean squared error on probabilities
- **Accuracy** — nearly useless for you, because a model that always says "pass" gets ~57%

Read the scikit-learn user guide sections on these. Compute all three for your baseline. Compute the "always predict the base rate" score too — that's your floor.

### Day 18 — Calibration
**Goal:** the concept that separates people who know what they're doing from people who don't.

A model is *calibrated* if, among plays it says are 70% pass, about 70% are actually passes. You need this, because your 4th down decision layer will multiply these probabilities by outcomes — an overconfident model produces confidently wrong recommendations.

- Read scikit-learn.org/stable/modules/calibration.html
- Plot a reliability curve for your baseline model (`CalibrationDisplay`)
- Save it to `figures/`

### Day 19 — Temporal splits
**Goal:** implement the split properly and understand why.

Train: 2016–2022. Validation: 2023. Test: 2024 — and don't touch 2024 again until the very end.

Write it as a function in `src/split.py` so you can't accidentally do it wrong later. Then, as an experiment, run a *random* split and see how much better your numbers look. Write that difference down — it's a great thing to be able to describe in an interview.

### Day 20 — Beat the public baseline
Compare your model's log loss against nflfastR's built-in `xpass` column on the same 2023 plays.

You will probably lose at first. That's fine and informative. Note where you lose most — likely obvious-passing-situation plays where their model has features you don't.

### Day 21 — Buffer

---

## Week 4 — Gradient boosting and the predictability index

### Day 22 — Gradient boosting, conceptually
- StatQuest: "Gradient Boost Part 1-4" and "XGBoost Part 1" (YouTube)
- Understand: residual fitting, why trees, what learning rate does, what `n_estimators` trades off against it

Don't write code today. Just understand it.

### Day 23 — Train the XGBoost model
`pip install xgboost`. Train on the same features and splits.

Use `early_stopping_rounds` with your 2023 validation set. Compare log loss to both your logistic baseline and `xpass`.

### Day 24 — Tuning without fooling yourself
**Goal:** learn how to tune without leaking your test set.

- Tune `max_depth`, `learning_rate`, `min_child_weight`, `subsample`
- Use the validation set for tuning, and only the validation set
- Learn what overfitting looks like in the train-vs-validation loss curves

Log every experiment in `notes/experiments.md`: settings, validation log loss. This is the habit that makes you look professional.

### Day 25 — Feature importance and SHAP
- `pip install shap`
- Make a SHAP summary plot for your model
- Learn the difference between "gain" importance and SHAP values, and why gain importance is misleading

Sanity check: does the model rely on `down` and `ydstogo` most? If something weird is at the top, you may have a leak.

### Day 26 — Define predictability
**Goal:** turn model confidence into a metric. This is your original contribution — spend real thought here.

Candidate definition: for each play, predictability = `1 - H(p)`, where `H` is the binary entropy of the model's predicted pass probability. A 50/50 prediction has maximum entropy (unpredictable); a 95% prediction has low entropy (predictable).

Write down in your notes why you chose your definition and what its weaknesses are. One weakness to think about: this measures *situational* predictability, not team-specific tendency. How would you separate those?

### Day 27 — Team-season leaderboard
Aggregate predictability by team and season. Make the leaderboard chart. Sanity check it against your football knowledge — do the teams at the extremes make sense to you? If a team looks wrong, dig in.

### Day 28 — Buffer

---

## Week 5 — The conversion model and the actual finding

### Day 29 — Build the conversion dataset
**Goal:** predict P(convert) on 3rd and 4th down.

Pool 3rd and 4th down attempts with a `down` indicator — there are only a few hundred 4th down go-attempts per season, not enough on their own.

Filter to actual attempts (not punts or FGs). Label: did they gain `ydstogo`? Note the **selection bias** in your notes: teams choose to go for it when they think they'll convert, so this sample isn't random. You can't fully fix this, but you should be able to articulate it.

### Day 30 — Rolling team-quality features
**Goal:** the leakage trap we discussed.

Build features like "offensive EPA/play over the previous 8 games" — computed *as of* that game, never season-long. Do the same for defensive EPA/play allowed.

This is fiddly pandas (`groupby` + `rolling` + `shift`). Budget the full hour. The `.shift(1)` is what prevents the current game leaking into its own feature — make sure you understand why it's there.

### Day 31 — Train the conversion model
XGBoost, same discipline: temporal split, log loss, early stopping. Baseline to beat: conversion rate by `ydstogo` bucket alone.

### Day 32 — Calibrate it
Reliability curve for the conversion model. This one matters more than the play-call model's, because your decision layer multiplies by it.

If it's poorly calibrated, look at `CalibratedClassifierCV` with isotonic or sigmoid calibration.

### Day 33 — The core test
Add your predictability index (from the offense's prior games, not the current play) as a feature to the conversion model.

Does log loss improve? What's the SHAP direction — does higher predictability mean lower conversion probability?

**This is the day your project either has a finding or doesn't.** Both outcomes are publishable; a well-argued null result is much better than a fake positive.

### Day 34 — Confounders
**Goal:** the question an interviewer will ask.

"Isn't this just that good teams are less predictable?" Test it:
- Is predictability correlated with offensive EPA/play?
- Does the effect survive when you control for team quality?
- Split by distance — is the effect concentrated in short yardage?

Write your answers in `notes/analysis.md`.

### Day 35 — Buffer

---

## Week 6 — Decision layer and writeup

### Day 36 — Decision theory framing
**Goal:** understand what you're computing before you compute it.

For a 4th down, you compare three expected win probabilities:

```
E[WP | go]   = P(convert) × WP(1st down at current spot)
             + (1 - P(convert)) × WP(opponent ball at current spot)

E[WP | FG]   = P(make) × WP(kickoff, up 3)
             + (1 - P(make)) × WP(opponent ball at spot)

E[WP | punt] = E over net punt distance of WP(opponent ball at resulting spot)
```

Read Ben Baldwin's writeups on the nflfastR 4th down model (search "Ben Baldwin 4th down bot"). Understand his approach before building yours.

### Day 37 — Punt and FG models
You don't need fancy models here. Empirical distributions are fine and defensible:
- FG: make rate by distance bucket (or a simple logistic on distance)
- Punt: distribution of net punt yards by field position bucket

Document that you chose empirical estimates deliberately.

### Day 38 — The decision function
Write `src/decide.py`: takes a game state, returns the three expected WPs and a recommendation.

Use nflfastR's `wp` column to build a lookup for win probability at a given state, rather than training your own WP model — that's a separate multi-week project and it's fine to stand on their shoulders as long as you say so.

### Day 39 — Backtest 2024
Run your model on every real 4th down in 2024. For each, compute the WP cost of the decision actually made vs. your recommendation. Aggregate by team.

**Now** is when you finally touch the test set. Report your model metrics on 2024 for the first time.

### Day 40 — Report figures
Build the 4–6 charts that carry your argument. Consistent style, labeled axes, readable without the caption. Save to `figures/`.

### Day 41 — Write the report
`REPORT.md` in the repo:
1. The question
2. Data and methods (including your leakage precautions — this is a selling point, say it explicitly)
3. The predictability index and how it's defined
4. The finding, with charts and honest uncertainty
5. The decision model and 2024 backtest
6. Limitations (selection bias, using nflfastR's WP, what you'd do with more time)

### Day 42 — Polish
Clean the README: what it is, how to run it, key findings up top with one chart embedded. Make sure a stranger can clone it and reproduce your results. Final commit.

---

## After Day 42 — optional modules, in order of value

1. **A small Flask app** (~1 week) — form input, returns the recommendation. Now it's a thin wrapper over work that already exists.
2. **A C inference engine** (~1 week) — export the trained trees, write a pure-C predictor, verify it matches Python bit for bit. Unusual, and it makes the project legible to hardware interviewers.
3. **The PyTorch sequence model** (~2 weeks) — LSTM over the sequence of plays in a drive, to capture setup effects a per-play model can't see.

If you're targeting hardware internships, **module 2 is the one that pays.** "I trained a model in Python and reimplemented inference in C to validate numerical equivalence" is a sentence that gets you asked about fixed-point arithmetic in an interview — which is exactly where you want the conversation to go.
