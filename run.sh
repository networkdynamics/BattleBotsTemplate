#!/bin/bash

# Set base_url and authentication_token from command line arguments
# export BASE_URL=$1  
#http://localhost:3000
# export AUTH_TOKEN=$2
#BOT: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0ZWFtSWQiOiIxIiwidGVhbU5hbWUiOiJCb3QxIiwiaWF0IjoxNzI0NjQ0MTQzLCJleHAiOjE3MjQ3MzA1NDN9.09K-DBNfF7fKFmFwifsu2fi5hSX4iRogbYaZQMEMJKg
#DETECTOR: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0ZWFtSWQiOiIzIiwidGVhbU5hbWUiOiJEZXRlY3RvcjEiLCJpYXQiOjE3MjQ0NDIxMTYsImV4cCI6MTcyNDUyODUxNn0.-qXvRUh8Qm0zq-hveZOni2nKs-onzQ7ubPyQF-Aji3M

# Run script
python3 BotTemplate/main_bot.py 
#python3 DetectorTemplate/main_detector.py

#To run run.sh enter this command in the prompt: sh run.sh <BASE_URL> <AUTH_TOKEN>