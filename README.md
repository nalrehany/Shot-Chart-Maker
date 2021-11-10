# Shot Chart Maker
Utilizing nba_api and some of venkatesannaveen's existing framework, I created the funciton that requires 4 inputs:
* Player first name
* Player last name
* Team
* Season

And from there, you have a shotchart showing Field Goals Made (FGM) for a given player in a given season.

## What Was Used

* nba_api by Ken Jee
* Pandas
* matplotlib
* json
* requests

	
## Using the API
nba_api utilizes endpoints that contain different families of basketball statistics. For example, in this project, the scores after each quarter were required, leading to the use of the scoreboard endpoint. However, there exists endpoints for virtually any family of statistics ranging from the defensive stats of a player in a certain game to something more general like franchise leaders. 
