# Import packages
from nba_api.stats.endpoints import shotchartdetail
from nba_api.stats.static import players
from nba_api.stats.static import teams
import json
import requests
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt


def shotchartmaker(player_firstname, player_lastname, team_name, season):
    
    # Load a json with player names and ID's as the shotchartdetail requires an ID 
    players = json.loads(requests.get('https://raw.githubusercontent.com/bttmly/nba/master/data/players.json').text)
     
    # Retrieve player ID when given a name
    def get_player_id(player_firstname, player_lastname):
        for player in players:
            if player['firstName'] == player_firstname and player['lastName'] == player_lastname:
                return player['playerId']
        return -1
    
    # Load json with team names and ID's as the shotchartdetail required as ID
    teams = json.loads(requests.get('https://raw.githubusercontent.com/bttmly/nba/master/data/teams.json').text)

    # Retrieve team ID when given a team name
    def get_team_id(team_name):
        for team in teams:
            if team['teamName'] == team_name:
                return team['teamId']
        return -1

    # JSON request
    shot_json = shotchartdetail.ShotChartDetail(
                team_id = get_team_id(team_name),
                player_id = get_player_id(player_firstname, player_lastname),
                context_measure_simple = 'FGM',
                season_nullable = season,
                season_type_all_star = 'Regular Season')

    # Load the given data into a dict
    shot_data = json.loads(shot_json.get_json())

    # Relevant data contains only necessary data for this analysis, omitting those not needed
    relevant_data = shot_data['resultSets'][0]
    # Retrieve headers and rows
    headers = relevant_data['headers']
    rows = relevant_data['rowSet']

    # Create pandas DataFrame
    chosen_player = pd.DataFrame(rows)
    chosen_player.columns = headers

    def create_court(ax, color):

        # Short corner 3PT lines
        ax.plot([-220, -220], [0, 140], linewidth=2, color=color)
        ax.plot([220, 220], [0, 140], linewidth=2, color=color)

        # 3PT Arc
        ax.add_artist(mpl.patches.Arc((0, 140), 440, 315, theta1=0, theta2=180, facecolor='none', edgecolor=color, lw=2))

        # Lane and Key
        ax.plot([-80, -80], [0, 190], linewidth=2, color=color)
        ax.plot([80, 80], [0, 190], linewidth=2, color=color)
        ax.plot([-60, -60], [0, 190], linewidth=2, color=color)
        ax.plot([60, 60], [0, 190], linewidth=2, color=color)
        ax.plot([-80, 80], [190, 190], linewidth=2, color=color)
        ax.add_artist(mpl.patches.Circle((0, 190), 60, facecolor='none', edgecolor=color, lw=2))

        # Rim
        ax.add_artist(mpl.patches.Circle((0, 60), 15, facecolor='none', edgecolor=color, lw=2))

        # Backboard
        ax.plot([-30, 30], [40, 40], linewidth=2, color=color)

        # Remove ticks
        ax.set_xticks([])
        ax.set_yticks([])

        # Set axis limits
        ax.set_xlim(-250, 250)
        ax.set_ylim(0, 470)

        return ax

    # Plot customizations
    mpl.rcParams['font.family'] = 'Avenir'
    mpl.rcParams['font.size'] = 18
    mpl.rcParams['axes.linewidth'] = 2

    # Create figure and axes
    fig = plt.figure(figsize=(4, 3.76))
    ax = fig.add_axes([0, 0, 1, 1])

    # Draw court
    ax = create_court(ax, 'black')

    # Plot hexbin of shots
    ax.hexbin(chosen_player['LOC_X'], chosen_player['LOC_Y'] + 60, gridsize=(30, 30), extent=(-300, 300, 0, 940), bins='log', cmap='YlOrRd')

    # Annotate player name and season
    ax.text(0, 1.05, f'{player_firstname} {player_lastname}\n{season} FGM', transform=ax.transAxes,
            ha='left', va='baseline')

    # Save and show figure
    plt.savefig(f'{player_lastname}{season}', dpi=300, bbox_inches='tight')
    plt.show()

shotchartmaker('Stephen', 'Curry', 'Golden State Warriors', '2009-10')
