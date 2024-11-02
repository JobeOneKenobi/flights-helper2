from pprint import pprint

import openai
from dateutil import parser
from openai import OpenAI
import configparser
from datetime import datetime
import ast
import logging

# Configure logging to display messages in the console
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

checklist = {
    'home_airport': None,
    'destination': None,
    'departure_date': None,
    'return_date': None,
    'airline_preference': None,
}


def chat_flight_checklist_request_initial(user_message):
    '''
    Takes in any message from a user and parses it for relevant flight details
    :param user_message:
    :return:
    '''
    today = datetime.today().date()
    day_of_week = today.strftime('%A')

    # Any info you want to have chatgpt know for context
    pertinent_info = " ".join(["Today is", day_of_week, str(today)])

    # Format the system message with pertinent information
    system_message_content = f"""you are flight booking assistant text processor. based off context, match the users input to the most correct items from the following list:
    checklist = {{ 'home_airport': None, 'destination': None, 'departure_date': None, 'return_date': None, 'airline_preference': None }}
    Your response should follow the exact same formatting as the checklist, replacing None entries with data from the user's input
    Pertinent Information: {pertinent_info} Use the same date formatting in your responses. If only given one airport / location, assume it is the destination."""

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-16k",  # "gpt-4o-mini" -> 4o mini tends to fuck things up on formatting
        messages=[
            {
                "role": "system",
                "content": system_message_content
            },
            {
                "role": "user",
                "content": user_message
            }
        ],
        temperature=1,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    # add try / error code here:
    response_content = response.choices[0].message['content']
    logging.info(f"user flight info request parsed by ChatGPT {response_content}")

    # Chat response type is a string so need to convert it to a dictionary
    try:
        response_dictionary = ast.literal_eval(response_content)
    except Exception as error:
        # logging.info(f"ast.literal conversion triggered error: {error}")
        response_dictionary = {}

    return response_dictionary


def fix_dates(input_str):
    try:
        # Attempt to parse the date
        parsed_date = parser.parse(input_str, fuzzy=True, default=datetime.now())

        # Standardize the date format to YYYY-MM-DD
        standardized_date = parsed_date.strftime('%Y-%m-%d')

        return standardized_date
    except (ValueError, OverflowError):
        return None


if __name__ == '__main__':
    client = OpenAI()

    # Before pushing to heroku and making work over text, configure api key to be stored in heroku
    # Ask chat for help
    config = configparser.ConfigParser()
    config.read('config.ini')

    # Pull the api key from the config file
    openai_api_key = config['openai']['api_key']
    # Configure the api key
    openai.api_key = openai_api_key

    # For testing purposes, prompt the user, this will be text-based in final version
    # user_input = input('where would you like to go?')
    #
    # updated_flight_request_info = chat_flight_checklist_request_initial(user_input)
    # print('\n\n Updated travel information: ')
    # print(updated_flight_request_info)

    # AFTER I have chat process the user's input
    # THEN fill in missing values with pertinent info from the user's file
    # Then check if anything is still missing, if so send updated contents to chat and have it prompt the user
    # with new prompt to fill in remaining data

    user_message = input('gimme some info')

    ai_sifted_input_data = chat_flight_checklist_request_initial(user_message)

    pprint(ai_sifted_input_data)




