from flask import Flask, jsonify 
import requests
import os 

app = Flask(__name__)

#? Set serAPI URL and key
SERP_API_URL = "https://serpapi.com/search.json"
SERP_API_KEY = os.getenv("SPORTS_API_KEY")

@app.route('/sports', method=['GET'])
def get_nfl_schedule():
  try:
    #? Create query for the API
    params = {
      "engine": "google",
      "q": "nfl schedule",
      "api_key": SERP_API_KEY
    }
    #? Consume external API
    response = requests.get(SERP_API_URL, params=params)
    response.raise_for_status()
    #? Get data form API to json
    data = response.json()
    
    #? Extract the info from the API JSON request 
    games = data.get("sports_result", {}).get("games", [])
    if not games:
      return jsonify({"message": "No NFL schedule available", "games": []}), 200
    
    #? There are available games 
    formatted_games = []
    for game in games: 
      teams = game.get("teams", [])
      if len(teams) == 2:
        away_team = teams[0].get("name", "Unknown")
        home_team = teams[1].get("name", "Unknown")
      else:
        away_team, home_team = "Unknown", "Unknown"
      
      game_info = {
        "away_team": away_team,
        "home_team": home_team,
        "venue": game.get("venue", "Unknown"),
        "date": game.get("date", "Unknown"),
        "time": f'game.get("time", "Unknown") ET' if game.get("time", "Unknown") != "Unknown" else "Unknown" 
      }    
      formatted_games.append(game_info)
    return jsonify({"messsage": "NFL schedule fetched succesfully", "games": formatted_games}), 200
  except Exception as e:
    return jsonify({"message": "An error occurred", "error": str(e)}), 500
  
if __name__ == "__main__":
  app.run(host='0.0.0.0', port=8080)