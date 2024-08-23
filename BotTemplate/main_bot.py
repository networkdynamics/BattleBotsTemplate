import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import requests
import json
from BotCode.bot import Bot
import logging
import signal
from constants import bot_session_id, bot_code_max_time
from pydantic import ValidationError
from teams_classes import User
from api_requests import get_session_info, create_user_id, get_sub_session, submit_injection


logging.basicConfig(
    filename='BotTemplate/run.log',
    filemode='w',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class TimeoutError(Exception):
    """Custom exception for timeout errors."""
    pass

def handler(signum, frame):
    raise TimeoutError("Timeout Error:")

def main():
    try:
        logging.info(f"START SESSION {bot_session_id}")
        bot = Bot()
        # Get session info for the present session
        #session_info = requests.get(base_url + '/api/bot/session/' + str(bot_session_id) + '/info', headers=header)
        session_info_response, session_info = get_session_info()
        # Verify if response was successful for sessionInfo_response
        session_info_response.raise_for_status()
        # Print the response output
        logging.info(f"Session Info response status code: {session_info_response.status_code}")
        print("Session Info response status code:", session_info_response.status_code)
        #print(f"Session Info output: {json.dumps(session_info_response.json(), indent=4)}\n- - - - -")

        # Give the session info to the bot teams and the id of the present sub_session and receive from there createUser
        # function the amount of users they want
        signal.signal(signal.SIGALRM, handler)
        signal.alarm(bot_code_max_time)

        new_users = bot.create_user(session_info)
        number_users = len(new_users)

        # Create the users for the team according to their response, the default value should be 1
        #users_id_list = requests.post(base_url + '/api/bot/session/' + str(bot_session_id) + '/createuser', headers=header, data=json.dumps({"num_of_users": number_users}))
        create_user_response, users_id_list = create_user_id(number_users)
        # Verify if response was successful for createUser_response
        create_user_response.raise_for_status()
        # Print the response output
        logging.info(f"Create User response status code: {create_user_response.status_code}")
        print("Create User response status code:", create_user_response.status_code)
        #print(f"Create User output: {json.dumps(create_user_response.json(), indent=4)}\n- - - - -")

        #Make the Users list
        bot_users = []
        for i in range(len(new_users)):
            bot_users.append(User(user_id=str(users_id_list[i]), username=new_users[i].username, name=new_users[i].name, description=new_users[i].description, location=new_users[i].location)) # Test if username and co have to be string or not later.

        for sub_session in session_info.sub_sessions_id:
            # Get the team sub-session posts dataset and users dataset
            #sub_session_dataset = requests.get(base_url + '/api/bot/session/' + str(bot_session_id) + '/' + str(sub_session), headers=header)
            get_sub_response, sub_session_dataset = get_sub_session(sub_session)
            # Verify if response was successful for getSubSession_response
            get_sub_response.raise_for_status()
            # Print the response output
            logging.info(f"Get Sub-Session response status code: {get_sub_response.status_code}")
            print("Get Sub-Session response status code:", get_sub_response.status_code)
            #print(f"Get Sub-Session output:{json.dumps(get_sub_response.json(), indent=4)}\n- - - - -")

            # Give the datasets and the list of users id to the team and make them start the run of their code and timeout if too long
            # Run subSessionInjection
            try:
                team_submission = bot.generate_content(sub_session_dataset, bot_users)
            except TimeoutError as exc:
                logging.error(f"{exc} The generate_content code for sub-session {sub_session} ran for too long. Continuing with an empty response.")
                team_submission = json.dumps({"posts": [], "users": []})
            
            signal.alarm(0)
            
            # Make the json submission (should probably also check here for any weird trick in post text and all)
            posts_submission = [post.to_dict() for post in team_submission]
            users_submission = [user.to_dict() for user in bot_users]
            # Inject the new posts and users in the session dataset
            #submission_confirmation = requests.post(base_url + '/api/bot/session/' + str(bot_session_id) + '/' + str(sub_session), headers=header, data=json.dumps({"posts": posts_submission, "users": users_submission}))
            submission_confirmation = submit_injection(sub_session, posts_submission, users_submission)
            # Verify if response was successful for injectSubSession_response
            submission_confirmation.raise_for_status()
            # Print the response output
            logging.info(f"Inject Sub-Session response status code: {submission_confirmation.status_code}")
            print("Inject Sub-Session response status code:", submission_confirmation.status_code)
            #print(f"Inject Sub-Session output: {json.dumps(submission_confirmation.json(), indent=4)}\n- - - - -")
        # Maybe add time stamp for analysis.
        logging.info(f"END SESSION {bot_session_id}")

    except (requests.exceptions.RequestException, ValidationError, TimeoutError) as exc:
        if isinstance(exc, requests.exceptions.RequestException):
            logging.error(f"An error occured: {exc}")
            print("An error occurred:", exc)
        elif isinstance(exc, ValidationError):
            logging.error(exc.errors())
            print(exc.errors())
        elif isinstance(exc, TimeoutError):
            logging.error(f"{exc} The code to Create User ran for too long. No submission were able to be submitted.")
            print(f"{exc} The code to Create User ran for too long. No submission were able to be submitted.")

if __name__ == "__main__":
    main()

# To be automated: f
# - getting the authentication token 
# - getting the session id

# To maybe modify:
# - the timeout might not work on other computer system so we might have to look for an alternative
# - some minor change might be done here depending on which metadata we give
# - any other analysis information that could be useful like the time it took for each sub-session or others
