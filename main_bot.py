import requests
import json
import bot
import multiprocessing
import time

session_id = 1
# API endpoint URL
baseUrl = 'https://wise-vans-itch.loca.lt'
# Authentication token to know which team we are dealing with and make the requests
authenticationToken = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0ZWFtSWQiOiIzIiwidGVhbU5hbWUiOiJFbWlsaWUgQm90IiwiaWF0IjoxNzIyMzYxNzU1LCJleHAiOjE3MjI0NDgxNTV9.TT1eCOlE8X1R5FosbmL9HqqtvDbgfs4P4Fy1dZ9NnCg'
header = {'Authorization': 'bearer ' + authenticationToken, 'Content-Type': 'application/json'}
sub_sessions_id = []

def run_with_timeout(func, args, timeout):
    pool = multiprocessing.Pool(processes=1)
    result = pool.apply_async(func, args)
    try:
        return result.get(timeout=timeout)
    except multiprocessing.TimeoutError:
        pool.terminate()
        return {}  # Return an empty dictionary if timeout occurs
    finally:
        pool.close()
        pool.join()

try:
    # Get session info for the present session
    sessionInfo_response = requests.get(baseUrl + '/api/bot/session/' + str(session_id) + '/info', headers=header)
    # Verify if response was successful for sessionInfo_response
    sessionInfo_response.raise_for_status()
    # Print the response output
    print("sessionInfo response status code:", sessionInfo_response.status_code)
    print(sessionInfo_response.json())

    # Get the sub-session id from the get info.
    sub_sessions_id = [1, 2, 3, 4]
    # Give the session info to the bot teams and the id of the present sub_session and receive from there createUser
    # function that can process the information the amount of users they want according to that info
    team_user_response = bot.createUser(sessionInfo_response.json())
    print(team_user_response) # To verify that it is an int and debugging

    # Create the users for the team according to their response, the default value should be 1
    createUser_response = requests.post(baseUrl + '/api/bot/session' + str(session_id) + '/createuser', headers=header, data=team_user_response)
    # Verify if response was successful for createUser_response
    createUser_response.raise_for_status()
    # Print the response output
    print("createUser response status code:", createUser_response.status_code)
    print(createUser_response.json())

    for sub_session in sub_sessions_id:
        # Get the team sub-session posts dataset and users dataset
        getSubSession_response = requests.get(baseUrl + '/api/bot/session/' + str(session_id) + '/' + str(sub_session), headers=header)
        # Verify if response was successful for getSubSession_response
        getSubSession_response.raise_for_status()
        # Print the response output
        print("getSubSession response status code:", getSubSession_response.status_code)
        print(getSubSession_response.json())

        # Give the datasets and the list of users id to the team and make them start the run of their code and timeout if too long
        # Run subSessionInjection with a 30-minute timeout
        team_injection_response = run_with_timeout(bot.subSessionInjection, (sub_session, getSubSession_response, createUser_response), timeout=1800)
        if not team_injection_response:
            print(f"Timeout occurred for sub-session {sub_session}. Continuing with an empty response.")

        # Inject the new posts and users in the session dataset
        injectSubSession_response = requests.post(baseUrl + '/api/bot/session/' + str(session_id) + '/' + str(sub_session), headers=header, data=team_injection_response)
        # Verify if response was successful for injectSubSession_response
        injectSubSession_response.raise_for_status()
        # Print the response output
        print("injectSubSession response status code:", injectSubSession_response.status_code)
        print(injectSubSession_response.json())
    # Maybe add time stamp for analysis.

except requests.exceptions.RequestException as err:
    print("An error occurred:", err)