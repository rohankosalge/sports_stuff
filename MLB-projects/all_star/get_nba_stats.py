from bs4 import BeautifulSoup
from urllib.request import urlopen
import requests
import pandas as pd
from http.client import IncompleteRead

id_lookup_data = pd.read_csv('/Users/rohankosalge/Desktop/Coding/NBA-projects/player_id_lookup_since_2020.csv').values.tolist()
id_lookup = {}
for row in id_lookup_data:
    id_lookup[row[0]] = row[2]


def pretty_to_num(date):
    month_to_num = {'JAN':'01','FEB':'02','MAR':'03','APR':'04',
                    'MAY':'05','JUN':'06','JUL':'07','AUG':'08',
                    'SEP':'09','OCT':'10','NOV':'11','DEC':'12'}
    return date[-4:]+month_to_num[date[:3]]+str(date[5:7])

def get_data(url, with_header = False):
    # get data, given the url and using the html web scraping module
    try:
        page = urlopen(url).read()
    except IncompleteRead as e:
        page = e.partial
        
    soup = BeautifulSoup(page, features='lxml')
    
    rows = soup.findAll('tr')[:]

    if with_header:
        rows_data = [[td.getText() for td in row.findAll('th')] + [td.getText() for td in row.findAll('td')]  for row in rows]
    else:
        rows_data = [[td.getText() for td in row.findAll('td')]  for row in rows]
    
    return rows_data

def get_data_headers(url):
    soup = BeautifulSoup(urlopen(url), features='lxml')
    rows = soup.findAll('tr')[:]

    return [[td.getText() for td in row.findAll('th')]  for row in rows]
    

def url_exists(url):
    response = requests.get(url)
    if response.status_code == 200:
        return True
    else:
        return False


def get_player_stat_avg(player, year, stat):
    # returns player stat average given a season and stat

    player_data = get_data('https://www.basketball-reference.com/leagues/NBA_'+str(year)+'_per_game.html')
    players = [player_stats[0].replace('*','') for player_stats in player_data]

    stats = ['Player', 'Position', 'Age', 'Team', 'Games', 'Games Started', 'Minutes', 'FG', 'FGA', 'FG%', '3P', '3PA',
             '3P%', '2P', '2PA', '2P%', 'eFG%', 'FT', 'FTA', 'FT%', 'ORB', 'DRB', 'TRB', 'AST', 'STL', 'BLK', 'TOV',
             'PF', 'PTS']

    if player not in players:
        return None
    else:
        return float(player_data[players.index(player)][stats.index(stat)])

def get_player_stat_total(player, year, stat):
    # returns player stat total given a season and stat
    
    player_data = get_data('https://www.basketball-reference.com/leagues/NBA_'+str(year)+'_totals.html')
    player_data = [player_stats for player_stats in player_data if len(player_stats) > 0]
    players = [player_stats[0].replace('*','') for player_stats in player_data]

    stats = ['Player', 'Position', 'Age', 'Team', 'Games', 'Games Started', 'Minutes', 'FG', 'FGA', 'FG%', '3P', '3PA',
             '3P%', '2P', '2PA', '2P%', 'eFG%', 'FT', 'FTA', 'FT%', 'ORB', 'DRB', 'TRB', 'AST', 'STL', 'BLK', 'TOV',
             'PF', 'PTS']

    if player not in players:
        return None
    else:
        return int(player_data[players.index(player)][stats.index(stat)])

def get_player_advanced(player, year, stat):
    # returns player advanced stat given season and stat

    raw_player_data = get_data('https://www.basketball-reference.com/leagues/NBA_'+str(year)+'_advanced.html')
    player_data = [row for row in raw_player_data if len(row) != 0]
    players = [player_stats[0].replace('*','') for player_stats in player_data]

    stats = ['Player', 'Position', 'Age', 'Team', 'Games', 'Minutes', 'PER', 'TS%', '3PAr', 'FTr', 'ORB%', 'DRB%', 'TRB%',
             'AST%', 'STL%', 'BLK%', 'TOV%', 'USG%', '', 'OWS', 'DWS', 'WS', 'WS/48', '', 'OBPM', 'DBPM', 'BPM', 'VORP']

    if player not in players:
        return None
    else:
        return float(player_data[players.index(player)][stats.index(stat)])

# convert team initial to full team name
init_to_tm = {
              'ATL': 'Atlanta Hawks', 'BRK': 'Brooklyn Nets', 'CHO': 'Charlotte Hornets', 'CHI': 'Chicago Bulls', 'CLE': 'Cleveland Cavaliers', 'DAL': 'Dallas Mavericks', 'HOU': 'Houston Rockets', 'DEN': 'Denver Nuggets', 'DET': 'Detroit Pistons',
              'GSW': 'Golden State Warriors', 'MEM': 'Memphis Grizzlies', 'MIA': 'Miami Heat', 'MIL': 'Milwaukee Bucks', 'NOP': 'New Orleans Pelicans', 'NYK': 'New York Knicks', 'ORL': 'Orlando Magic', 'OKC': 'Oklahoma City Thunder',
              'POR': 'Portland Trail Blazers', 'MIN': 'Minnesota Timberwolves', 'SAC': 'Sacramento Kings', 'PHO': 'Phoenix Suns', 'LAL': 'Los Angeles Lakers', 'LAC': 'Los Angeles Clippers', 'TOR': 'Toronto Raptors', 'WAS': 'Washington Wizards',
              'UTA': 'Utah Jazz', 'IND': 'Indiana Pacers', 'PHI': 'Philadelphia 76ers', 'SAS': 'San Antonio Spurs', 'BOS': 'Boston Celtics',

              'PIT': 'Pittsburgh Ironmen', 'DTF': 'Detroit Falcons', 'CHS': 'Chicago Stags', 'STB': 'St. Louis Bombers',
              'CLR': 'Cleveland Rebels', 'PRO': 'Providence Steamrollers', 'PHW': 'Philadelphia Warriors',
              'TRH': 'Toronto Huskies', 'WSC': 'Washington Capitols', 'BLB': 'Baltimore Bullets',
              'FTW': 'Fort Wayne Pistons', 'INJ': 'Indianapolis Jets', 'MNL': 'Minneapolis Lakers',
              'ROC': 'Rochester Royals', 'SHE': 'Sheboygan Redskins', 'INO': 'Indianapolis Olympians',
              'AND': 'Anderson Packers', 'WAT': 'Waterloo Hawks', 'DNN': 'Denver Nuggets', 'SYR': 'Syracuse Nationals',
              'TRI': 'Tri-Cities Blackhawks', 'MLH': 'Milwaukee Hawks', 'STL': 'St. Louis Hawks',
              'CIN': 'Cincinnati Royals', 'CHP': 'Chicago Packers', 'SFW': 'San Francisco Warriors',
              'CHZ': 'Chicago Zephyrs', 'BAL': 'Baltimore Bullets', 'SDR': 'San Diego Rockets',
              'SEA': 'Seattle Supersonics', 'BUF': 'Buffalo Braves', 'KCO': 'Kansas City-Omaha Kings',
              'CAP': 'Capital Bullets', 'NOJ': 'New Orleans Jazz', 'KCK': 'Kansas City Kings',
              'WSB': 'Washington Bullets', 'NYN': 'New York Nets', 'NJN': 'New Jersey Nets',
              'SDC': 'San Diego Clippers', 'CHH': 'Charlotte Hornets', 'VAN': 'Vancouver Grizzlies',
              'NOH': 'New Orleans Hornets', 'CHA': 'Charlotte Bobcats', 'NOK': 'NO/Oklahoma City Hornets'
              }

# convert full team name to team initial (modern version -- since 2015)
tm_to_init = {
              'Atlanta Hawks': 'ATL', 'Brooklyn Nets': 'BRK', 'Charlotte Hornets': 'CHO', 'Cleveland Cavaliers': 'CLE', 'Dallas Mavericks': 'DAL', 'Houston Rockets': 'HOU', 'Denver Nuggets': 'DEN', 'Detroit Pistons': 'DET',
              'Golden State Warriors': 'GSW', 'Memphis Grizzlies': 'MEM', 'Miami Heat': 'MIA', 'Milwaukee Bucks': 'MIL', 'New Orleans Pelicans': 'NOP', 'New York Knicks': 'NYK', 'Orlando Magic': 'ORL', 'Oklahoma City Thunder': 'OKC',
              'Portland Trail Blazers': 'POR', 'Minnesota Timberwolves': 'MIN', 'Sacramento Kings': 'SAC', 'Phoenix Suns': 'PHO', 'Los Angeles Lakers': 'LAL', 'Los Angeles Clippers': 'LAC', 'Toronto Raptors': 'TOR',
              'Washington Wizards': 'WAS', 'Utah Jazz': 'UTA', 'Indiana Pacers': 'IND', 'Philadelphia 76ers': 'PHI', 'San Antonio Spurs': 'SAS', 'Boston Celtics': 'BOS', 'Chicago Bulls': 'CHI', 'New Orleans Hornets': 'NOH',
              'New Jersey Nets': 'NJN', 'New Orleans/Oklahoma City Hornets': 'NOK', 'Charlotte Bobcats': 'CHA', 'Seattle SuperSonics': 'SEA', 'Washington Bullets': 'WSB', 'Kansas City Kings': 'KCK', 'Vancouver Grizzlies': 'VAN'
             }


# assigns team name to their respective colors.
team_to_colors = {"Atlanta Hawks": ["#E03A3E", "#C1D32F", "#26282A"],
                  "Boston Celtics": ["#007A33", "#FFFFFF", "#000000"],
                  "Brooklyn Nets": ["#000000", "#FFFFFF"],
                  "Charlotte Hornets": ["#1D1160", "#00788C", "#A1A1A4"],
                  "Chicago Bulls": ["#CE1141", "#000000"],
                  "Cleveland Cavaliers": ["#860038", "#FDBB30", "#041E42", "#000000"],
                  "Dallas Mavericks": ["#00538C", "#FFFFFF", "#000000", "#002B5E", "#B8C4CA"],
                  "Denver Nuggets": ["#0E2240", "#FEC524", "#8B2131", "#1D428A"],
                  "Detroit Pistons": ["#BEC0C2", "#1D42BA", "#C8102E", "#002D62"],
                  "Golden State Warriors": ["#1D428A", "#FFC72C"],
                  "Houston Rockets": ["#CE1141", "#000000", "#C4CED4"],
                  "Indiana Pacers": ["#002D62", "#FDBB30", "#BEC0C2"],
                  "Los Angeles Clippers": ["#1D428A", "#FF0000", "#C8102E","#BEC0C2", "#000000"],
                  "Los Angeles Lakers": ["#552583", "#FDB927", "#000000"],
                  "Memphis Grizzlies": ["#5D76A9", "#12173F", "#F5B112", "#707271"],
                  "Miami Heat": ["#98002E", "#F9A01B", "#000000"],
                  "Milwaukee Bucks": ["#00471B", "#EEE1C6", "#000000"],
                  "Minnesota Timberwolves": ["#0C2340", "#236192", "#9EA2A2", "#78BE20"],
                  "New Orleans Pelicans": ["#0C2340", "#85714D", "#C8102E"],
                  "New York Knicks": ["#006BB6", "#F58426", "#BEC0C2", "#000000"],
                  "Oklahoma City Thunder": ["#EF3B24", "#1E3160", "#007EC2", "#002D62", "#FDBB30"],
                  "Orlando Magic": ["#0077C0", "#C4CED4", "#000000"],
                  "Philadelphia 76ers": ["#006BB6", "#FFFFFF", "#C4CED4", "#ED174C"],
                  "Phoenix Suns": ["#1D1160", "#E56020", "#000000", "#63727A", "#F9AD1B"],
                  "Portland Trail Blazers": ["#E03A3E", "#000000"],
                  "Sacramento Kings": ["#5A2D81", "#63727A", "#000000"],
                  "San Antonio Spurs": ["#C4CED4", "#000000"],
                  "Toronto Raptors": ["#CE1141", "#000000", "#A1A1A4", "#B4975A"],
                  "Utah Jazz": ["#F9A01B", "#00471B", "#002B5C"],
                  "Washington Wizards": ["#002B5C", "#E31837", "#C4CED4"],
                  "Washington Bullets": ["#002B5C", "#E31837", "#C4CED4"],
                  "Vancouver Grizzlies": ["#40E0D0", "#CD7F32"],
                  "New Orleans Hornets": ["#29B6F6", "#FFCA28"],
                  "New Orleans/Oklahoma City Hornets": ["#29B6F6", "#FFCA28"],
                  "New Jersey Nets": ["#90A4AE", "#1A237E"],
                  "Seattle Supersonics": ["#046A3B", "#FFA300"],
                  "Charlotte Bobcats": ["#306EB0", "#F26A1B", "#BABDC2"]}

def team_to_initial(team, season):
    if team == 'Charlotte Hornets':
        if season < 2006:
            return 'CHH'
        else:
            return 'CHO'
    else:
        return tm_to_init[team]
    
# initialize stat dictionaries
# user enters year, and all the players in that season are mapped to their stats
global get_totals
global get_pergame
global get_per36
global get_per100
global get_advanced
global get_adjshooting

get_totals = {}
get_pergame = {}
get_per36 = {}
get_per100 = {}
get_advanced = {}
get_adjshooting = {}


# helper function, addon to make_stat_dicts
def make_stat_dict(url, stat_dict):
    data = get_data(url)
    for row in data:
        if row == []:
            continue
        if row[3] == 'TOT':
            continue
        if (row[0], row[3]) not in stat_dict:
            stat_dict.update({(row[0], row[3]):row[1:3]+row[4:]})
    return stat_dict
    
def make_stat_dict_simple(url, stat_dict):
    data = get_data(url)
    for row in data:
        if row == []:
            continue
        if row[3] == 'TOT':
            continue
        if (row[0], row[3]) not in stat_dict:
            stat_dict.update({row[0]:row[1:3]+row[4:]})
    return stat_dict

# call this function before any other; allows for more efficient search
def make_stat_dicts(year):
    global get_totals
    global get_pergame
    global get_per36
    global get_per100
    global get_advanced
    global get_adjshooting
    
    year = str(year)
    get_totals = make_stat_dict_simple("https://www.basketball-reference.com/leagues/NBA_"+year+"_totals.html", get_totals)
    get_pergame = make_stat_dict_simple("https://www.basketball-reference.com/leagues/NBA_"+year+"_per_game.html", get_pergame)
    get_per36 = make_stat_dict_simple("https://www.basketball-reference.com/leagues/NBA_"+year+"_per_minute.html", get_per36)
    get_per100 = make_stat_dict_simple("https://www.basketball-reference.com/leagues/NBA_"+year+"_per_poss.html", get_per100)
    get_advanced = make_stat_dict_simple("https://www.basketball-reference.com/leagues/NBA_"+year+"_advanced.html", get_advanced)
    get_adjshooting = make_stat_dict_simple("https://www.basketball-reference.com/leagues/NBA_"+year+"_adj_shooting.html", get_adjshooting)


# get all players who played in a given year
def get_players(year):
    year = str(year)
    global get_totals
    #get_totals.clear()
    
    get_totals = make_stat_dict("https://www.basketball-reference.com/leagues/NBA_"+year+"_totals.html", get_totals)

    return [name[0].replace('*','') for name in list(get_totals.keys())]
    

# use the get_data() function to receive stats

def get_ortg(player):
    return float(get_per100[player][-2]) if get_per100[player][-2] != "" else 0

def get_drtg(player):
    return float(get_per100[player][-1]) if get_per100[player][-1] != "" else 0

def get_nrtg(player):
    return float(get_ortg(player)) - float(get_drtg(player))

def get_ws(player):
    return float(get_advanced[player][-7])

def get_ws48(player):
    return float(get_advanced[player][-6])

def get_vorp(player):
    return float(get_advanced[player][-1])

def get_games(player):
    return float(get_totals[player][2])

def get_minutes(player):
    return float(get_pergame[player][4])

def get_usage_rate(player):
    return float(get_advanced[player][-11]) if get_advanced[player][-11] != "" else 0

def get_ppg(player):
    return float(get_pergame[player][-1])

def get_apg(player):
    return float(get_pergame[player][-6])

def get_rpg(player):
    return float(get_pergame[player][-7])

def get_spg(player):
    return float(get_pergame[player][-5])

def get_bpg(player):
    return float(get_pergame[player][-4])

def get_fpg(player):
    return float(get_pergame[player][-2])

def get_tpg(player):
    return float(get_pergame[player][-3])

def get_ts_pct(player):
    return float(get_advanced[player][7]) if get_advanced[player][7] != "" else 0

def get_points(player):
    return float(get_totals[player][-1])

def get_assists(player):
    return float(get_totals[player][-6])

def get_rebounds(player):
    return float(get_totals[player][-7])

def get_steals(player):
    return float(get_totals[player][-5])

def get_blocks(player):
    return float(get_totals[player][-4])

def get_fouls(player):
    return float(get_totals[player][-2])

def get_turnovers(player):
    return float(get_totals[player][-3])

def get_fg_pct(player):
    return float(get_totals[player][7]) if get_totals[player][7] != "" else 0

def get_3p_pct(player):
    return float(get_totals[player][10]) if get_totals[player][10] != "" else 0

def get_ft_pct(player):
    return float(get_totals[player][17]) if get_totals[player][17] != "" else 0

def get_position(player):
    return get_totals[player][0]
