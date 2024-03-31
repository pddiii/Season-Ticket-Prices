import requests
import json
import pandas as pd
import warnings
import re
from pandas import json_normalize
from bs4 import BeautifulSoup

# This function grabs ticket data for home_teams from SeatGeek API
def get_tickets(home_team_name: str, start_date: str, end_date: str):
    with open('../seatgeek_api.txt', 'r') as file:
        client_id = file.readline().strip()
        client_secret = file.readline().strip()
    
    url = f"https://api.seatgeek.com/2/events?performers[home_team].slug={home_team_name}&datetime_utc.gte={start_date}&datetime_utc.lte={end_date}&client_id={client_id}&client_secret={client_secret}&per_page=100"

    response = requests.get(url)

    data = response.json()
    games = data['events'] # extracts the important information concerning ticket prices

    df = pd.DataFrame(games) # create a DataFrame
    # columns of interest
    columns = ['datetime_utc', 'performers', 'stats', 'url', 'score', 'description', 'event_promotion']
    df = df[columns]

    # Use this to convert list object within 'performers'        
    df = df.explode('performers')
    # flatten the json
    performers = pd.json_normalize(df['performers'])
    df = df.reset_index(drop=True) # reset index
    performers = performers.reset_index(drop=True)
    # add the column back to the data
    df = pd.concat([df.drop('performers', axis=1), performers], axis=1)
    # remove repeated 'url' and 'score' columns
    column_names = df.columns.to_list()
    column_names[2] = 'sg_url'
    column_names[3] = 'sg_score'
    df.columns = column_names
    df = df.drop(columns = ['score', 'url']) # remove the duplicate columns

    stats = pd.json_normalize(df['stats'])
    df = df.reset_index(drop=True)
    stats = stats.reset_index(drop=True)
    df = pd.concat([df.drop('stats', axis=1), stats], axis=1)

    event_promotion = pd.json_normalize(df['event_promotion'])
    df = df.reset_index(drop=True)
    event_promotion = event_promotion.reset_index(drop=True)
    df = pd.concat([df.drop('event_promotion', axis=1), event_promotion], axis=1)

    # determine which teams are away teams
    away_teams = df[df['home_team'] != True][['name']]
    away_teams = away_teams.reset_index(drop=True) # reset index

    # remove duplicate games and reset the index
    df = df.drop_duplicates(subset=['datetime_utc'], keep='first').reset_index(drop=True)
    # add the away team to the data as a new column
    df['away_team'] = away_teams

    # drop unnecessary columns
    df = df.drop(columns=['colors.all', 'colors.primary', 'divisions', 'taxonomies',
                            'dq_bucket_counts', 'description', 'image', 'id',
                            'has_upcoming_events', 'primary', 'image_attribution',
                            'home_venue_id', 'num_upcoming_events', 'image_license',
                            'popularity', 'home_team', 'image_rights_message',
                            'images.huge', 'stats.event_count', 'colors.iconic', 
                            'location.lat', 'location.lon'])

    away_column = df['away_team']
    # drop the original away_team column
    df = df.drop(columns=['away_team'], axis=1)
    # drop picture variables
    df = df.drop(df.columns[[19, 20, 21]], axis = 1)

    # insert the away_team column back into the DataFrame next to the home_team column
    df.insert(3, 'away_team', away_column)

    # rename the home_team column
    df = df.rename(columns={'name': 'home_team'})
    
    # create a csv file for the data
    df.to_csv(f'../{home_team_name}_tickets.csv', index=False)
    
    return None

# Example method call
get_tickets(home_team_name = 'philadelphia-phillies', start_date='2024-03-31', end_date='2024-11-01')