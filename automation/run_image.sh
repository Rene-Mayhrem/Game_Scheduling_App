#!/bin/bash
NFL_DIF="/home/mayhrem/devops-nba-challenge/Game_Scheduling_App/src"

docker build -t nfl-backend $NFL_DIF
docker run -p 5000:5000 nfl-backend
