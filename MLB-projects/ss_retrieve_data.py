from baseball_scraper import batting_stats
import espn_scraper as espn
from bs4 import BeautifulSoup 
from urllib.request import urlopen
from http.client import IncompleteRead

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

stats = espn.get_url('https://www.espn.com/mlb/stats/player/_/season/2022/seasontype/2')
#stats = get_data('https://www.espn.com/mlb/stats/player/_/season/2022/seasontype/2', True)
#stats = batting_stats(2017)

print(stats)