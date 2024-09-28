import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import requests
from BotCode.bot import Bot
import logging
import signal
from constants import bot_session_id, bot_code_max_time
from pydantic import ValidationError
from teams_classes import User, NewUser, NewPost
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

class UsernameAlreadyTakenError(Exception):
    """Custom exception for duplicate usernames."""
    pass

def handler(signum, frame):
    raise TimeoutError("Timeout Error:")

def main():
    try:
        logging.info(f"START SESSION {bot_session_id}")
        bot = Bot()
        # Get session info for the present session
        session_info_response, session_info = get_session_info()
        # Verify if response was successful for get_session_info
        session_info_response.raise_for_status()
        # Print the response output
        logging.info(f"Session Info response status code: {session_info_response.status_code}")
        print("Session Info response status code:", session_info_response.status_code)
        #print(f"Session Info output: {json.dumps(session_info_response.json(), indent=4)}\n- - - - -")

        # Give the session info to the bot teams and the id of the present sub_session and receive from their create_user
        # function their new users
        signal.signal(signal.SIGALRM, handler)
        signal.alarm(bot_code_max_time)
        
        
        new_users = bot.create_user(session_info)

        # Verify username unique
        for user in new_users:
            if user.username in session_info.usernames:
                raise UsernameAlreadyTakenError(f"UsernameAlreadyTakenError: Username need to be unique and the username {user.username} is already taken.")
            else:
                session_info.usernames.add(user.username)
        # Verify submission format    
        if len(new_users) == 0: # Empty submission
            raise ValueError(f"Need at least 1 user create. Right now list of users is empty.")
        elif not isinstance(new_users[0], NewUser): # If the teams don't return a list of NewUser instance/object.
            raise TypeError(f"The elements of the list should be NewUser instance not {type(new_users[0])}. Make sure to return a list[NewUser].")
        else:
            number_users = len(new_users)

        # Create the users id for the team according to their response
        create_user_response, users_id_list = create_user_id(number_users)
        # Verify if response was successful for create_user_id
        create_user_response.raise_for_status()
        # Print the response status
        logging.info(f"Create User response status code: {create_user_response.status_code}")
        print("Create User response status code:", create_user_response.status_code)
        #print(f"Create User output: {json.dumps(create_user_response.json(), indent=4)}\n- - - - -")

        #Make the Users list
        bot_users = []
        for i in range(len(new_users)):
            bot_users.append(User(user_id=str(users_id_list[i]), username=new_users[i].username, name=new_users[i].name, description=new_users[i].description, location=new_users[i].location)) # Test if username and co have to be string or not later.

        for sub_session in session_info.sub_sessions_id:
            # Get the team sub-session posts dataset and users dataset
            get_sub_response, sub_session_dataset = get_sub_session(sub_session)
            # Verify if response was successful for get_sub_session
            get_sub_response.raise_for_status()
            # Print the response status
            logging.info(f"Get Sub-Session response status code: {get_sub_response.status_code}")
            print("Get Sub-Session response status code:", get_sub_response.status_code)
            #print(f"Get Sub-Session output:{json.dumps(get_sub_response.json(), indent=4)}\n- - - - -")

            # Run generate_content to make the submission
            try:
                team_submission = bot.generate_content(sub_session_dataset, bot_users)
                if len(team_submission) == 0: # Empty submission
                    posts_submission = []
                elif not isinstance(team_submission[0], NewPost): # If the teams don't return a list of NewPost instance/object.
                    raise TypeError(f"The elements of the list should be NewPost instance not {type(team_submission[0])}. Make sure to return a list[NewPost].")
                else:
                    posts_submission = [post.to_dict(session_info.lang) for post in team_submission]
            except TimeoutError as exc:
                logging.error(f"{exc} The generate_content code for sub-session {sub_session} ran for too long. Continuing with no submission for sub-session {sub_session}.")
                break
            
            # Make the json submission
            users_submission = [user.to_dict() for user in bot_users]

            # Inject the new posts and users in the session dataset
            submission_confirmation = submit_injection(sub_session, posts_submission, users_submission)
            # Verify if response was successful for submit_injection
            submission_confirmation.raise_for_status()
            # Print the response status
            logging.info(f"Inject Sub-Session response status code: {submission_confirmation.status_code}")
            print("Inject Sub-Session response status code:", submission_confirmation.status_code)
            #print(f"Inject Sub-Session output: {json.dumps(submission_confirmation.json(), indent=4)}\n- - - - -")

        signal.alarm(0)
        # Maybe add time stamp for analysis.
        logging.info(f"END SESSION {bot_session_id}")

    except (requests.exceptions.RequestException, ValidationError, TimeoutError, ValueError, TypeError, UsernameAlreadyTakenError) as exc:
        if isinstance(exc, requests.exceptions.RequestException):
            logging.error(f"An error occured: {exc}")
            print("An error occurred:", exc)
        elif isinstance(exc, ValidationError):
            logging.error(f"Object Error: Error Description {exc.errors()}. Make sure you create your instance correctly.")
            print(f"Object Error: Error Description {exc.errors()}. Make sure you create your instance correctly.")
        elif isinstance(exc, TimeoutError):
            logging.error(f"{exc} The code to Create User ran for too long. No submission were able to be submitted.")
            print(f"{exc} The code to Create User ran for too long. No submission were able to be submitted.")
        elif isinstance(exc, (ValueError, TypeError, UsernameAlreadyTakenError)):
            logging.error(exc)
            print(exc)

if __name__ == "__main__":
    main()

# To be automated:
# - getting the authentication token 
# - getting the session id

