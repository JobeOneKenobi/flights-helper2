import openai
from openai import OpenAI
import configparser
from datetime import datetime

client = OpenAI()

# Before pushing to heroku and making work over text, configure api key to be stored in heroku
# Ask chat for help
config = configparser.ConfigParser()
config.read('config.ini')

today = datetime.today().date()
day_of_week = today.strftime('%A')

# Pull the api key from the config file
openai_api_key = config['openai']['api_key']
# Configure the api key
openai.api_key = openai_api_key

# Any info you want to have chatgpt know for context or from the user's preferences file
pertinent_info = " ".join(["Today is", day_of_week, str(today)])
print(pertinent_info)

# Format the system message with pertinent information
system_message_content = f"""you are flight booking assistant text processor. based off context, match the users input to the most correct items from the following list:
checklist = {{ 'home_airport': None, 'destination': None, 'departure_date': None, 'return_date': None, 'airline_preference': None }}
Your response should follow the exact same formatting as the checklist, replacing None entries with data from the user's input
Pertinent Information: {pertinent_info}"""

# For testing purposes, prompt the user, this will be text-based in final version
user_input = input('where would you like to go?')

response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo-16k",
    messages=[
        {
            "role": "system",
            "content": system_message_content
        },
        {
            "role": "user",
            "content": user_input
        }
    ],
    temperature=1,
    max_tokens=256,
    top_p=1,
    frequency_penalty=0,
    presence_penalty=0
)

print(response)
response_content = response.choices[0].message['content']
print('\n\n Updated travel information: ')
print(response_content)

# AFTER I have chat process the user's input
# THEN fill in missing values with pertinent info from the user's file
# Then check if anything is still missing, if so send updated contents to chat and have it prompt the user
# with new prompt to fill in remaining data