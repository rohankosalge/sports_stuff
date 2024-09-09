# Simple Stats Proj
# Visualizing Distribution of Receiving Plays in Season by NFL WR

import nfl_data_py as nfl
import numpy as np
import pandas as pd
from tkinter import *

regfont = ('Andale Mono', 20, 'normal')
labelfont = ('Andale Mono', 12, 'normal')
global cur_season
cur_season = None
global data
data = []
global graph_widgets
graph_widgets = []

master = Tk()
master.title('Distribution of Rec Yards')

canvas = Canvas(master, height=800, width=800, bd=0, highlightthickness=0, bg='grey10')
canvas.pack()

# widgets
canvas.create_text(15, 16, text='Enter Receiver: ', font=regfont, anchor=NW, fill='white')
name_entry = Entry(master, font=regfont, width=42, bg='grey10', fg='white', insertbackground='white')
canvas.create_window(220, 10, window=name_entry, anchor=NW)
canvas.create_text(15, 56, text='Enter Year: ', font=regfont, anchor=NW, fill='white')
season_entry = Entry(master, font=regfont, width=42, bg='grey10', fg='white', insertbackground='white')
canvas.create_window(220, 50, window=season_entry, anchor=NW)

# graph
canvas.create_line(20, 710, 780, 710, width=3, arrow='both', fill='white')
canvas.create_text(400, 770, text='Receiving Yards', font=regfont, fill='white')
canvas.create_text(20, 400, text='Frequency', font=regfont, fill='white', angle=90)


def compile_data(season):
    global data
    data = nfl.import_pbp_data([season], downcast=True, cache=False, alt_path=None)
    data = data[['play_id', 'game_id', 'home_team', 'away_team', 'season_type', 'week', 'yards_gained', 'air_yards', 'yards_after_catch', 'pass_length', 'receiver']]
    data = data.values.tolist()

def vis_data(metrics):
    global graph_widgets
    for widget in graph_widgets:
        canvas.delete(widget)
    for i in range(-3, 4):
        graph_widgets.append(canvas.create_text(400+(120*i), 725, text=round(metrics[0]+i*metrics[1], 1), font=labelfont, fill='white'))
    scale_factor = 510/max(metrics[2:])
    for i in range(-3, 3):
        bin = metrics[2:][i+3]
        height = bin*scale_factor
        graph_widgets.append(canvas.create_rectangle(400+(120*i), 710-height, 400+(120*(i+1)), 710, outline='white', width=2, fill='light blue'))
        graph_widgets.append(canvas.create_text(400+(120*(i+0.5)), 710-height-15, text=bin, font=labelfont, fill='white'))

def get_metrics(player_data):
    # Index -5: Total yards, -4: Air yards, -3: YAC
    yards_per_rec = [rec[-5] for rec in player_data]
    mean, std = np.mean(yards_per_rec), np.std(yards_per_rec)
    bins = []
    for i in range(-3, 3):
        lower_bound, upper_bound = mean+(i*std), mean+((i+1)*std)
        bin_count = 0
        for yards in yards_per_rec:
            if yards >= lower_bound and yards < upper_bound:
                bin_count += 1
        bins.append(bin_count)
    return [mean, std] + bins

def load_player_data(name):
    global data
    player_data = [catch for catch in data if (catch[-1] == name and not pd.isna(catch[-3]) and catch[4] == 'REG')]
    vis_data(get_metrics(player_data))

def retrieve_inputs(event):
    global cur_season
    name, season = name_entry.get().split(' ')[0][0] + '.' + ' '.join(name_entry.get().split(' ')[1:]), int(season_entry.get())
    #print(name, season)
    if season != cur_season:
        cur_season = season
        compile_data(season)
    load_player_data(name)

master.bind('<Return>', retrieve_inputs)

mainloop()