import pandas as pd

teams_sos = {}

games = pd.read_csv('/Users/rohankosalge/Downloads/2023_nfl_schedule.csv').values.tolist()
games = [[game[0], game[4], game[6]] for game in games]
games = [game for game in games if len(game[0]) <= 2]

ranks = {}
ranks_raw = pd.read_csv('/Users/rohankosalge/Downloads/2023_nfl_power_ranks.csv').values.tolist()[1:]
ranks_raw = [team[:-2] for team in ranks_raw]
for row in ranks_raw:
    ranks[row[0]] = row[1:]

for game in games:
    tm1, tm2 = game[1], game[2]
    if tm1 not in teams_sos:
        teams_sos[tm1] = [None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None]
    if tm2 not in teams_sos:
        teams_sos[tm2] = [None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None]
    week = int(game[0])-1
    teams_sos[tm1][week] = int(ranks[tm2][week])
    teams_sos[tm2][week] = int(ranks[tm1][week])

sos = []
for team in teams_sos:
    team_sos = []
    team_sos.append(team)
    weeks = teams_sos[team]
    team_sos = team_sos + weeks
    rank_sum = 0
    for game in weeks:
        if game == None:
            continue
        rank_sum += game
    team_sos.append(round(rank_sum/17, 1))
    sos.append(team_sos)

sos = sorted(sos, key = lambda x: x[0])

sos_df = pd.DataFrame(sos)
sos_df.to_csv('/Users/rohankosalge/Downloads/2023_sos.csv')

print('done')