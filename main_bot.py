import requests
import json
import bot
# I STILL NEED TO ADD THE RAISE ERROR PART OF THE CODE
session_id = 1
amount_of_sub_session = 4
# API endpoint URL
baseUrl = 'https://little-rabbits-move.loca.lt/'
# Authentication token to know which team we are dealing with and make the requests
authenticationToken = ''
header = {'Authorization': 'bearer ' + authenticationToken, 'Content-Type': 'application/json'}

for sub_session in range(amount_of_sub_session):
    sub_session_id = sub_session + 1
    if sub_session == 0:
        # Get session info for the present session
        sessionInfo_response = requests.get(baseUrl + '/api/bot/session/' + str(session_id) + '/info', headers=header)
        # Give the session info to the bot teams and the id of the present sub_session and receive from there createUser
        # function that can process the information the amount of users they want according to that info
        team_user_response = bot.createUser(sub_session_id, sessionInfo_response)
        # VERIFY HERE THAT THE TEAM_USER_RESPONSE IS AN INT! For this line we might already be doing it in the API call.
        # Create the users for the team according to their response, the default value should be 1
        createUser_response = requests.post(baseUrl + '/api/bot/session' + str(session_id) + '/createuser', headers=header, data=team_user_response)
        # Give the list of users id in json format to the teams
        bot.getUserIdList(createUser_response)
    # Get the team sub-session posts dataset and users dataset (HERE VERIFY THAT I'M USING THE GOOD API CALL)
    getSubSession_response = requests.get(baseUrl + '/api/bot/session/' + str(session_id) + '/' + str(sub_session_id) + '/getsubsession', headers=header)
    # Give the datasets to the team and make them start the run of their code. If it goes over the time limit stop it
    # at the time limit (should we separate it for them in advance?)
    team_injection_response = bot.subSessionInjection(sub_session_id, getSubSession_response)
    # Here again do we have to verify if the output has the good format or are we verifying in the API call?
    # Inject the new posts and users in the session dataset (HERE VERIFY THAT I'M USING THE GOOD API CALL)
    injectSubSession_response = requests.post(baseUrl + '/api/bot/session/' + str(session_id) + '/' + str(sub_session_id) + '/injectsubsession', headers=header, data=team_injection_response)
    # Then I've made the execution of the next sub-session start automatically in the flow instead of trying to
    # synchronize everyone since in this case I don't believe it would change something
# Now that each sub-session is done we finish the execution of the code, can send a finish signal to the image here
# maybe if it can help
