# Main function to run everything right now, still testing locally
from flights.fast_flights import FlightData, Passengers, create_filter, get_flights, Airport
# Importing the entire fast_flights module

import configparser
import openai
from openai import OpenAI
# My functions
from flight_times import find_shortest_flight
from check_airports import find_nearby_airports
from checklist_logic_ai import chat_flight_checklist_request_initial
from checklist_logic import checklist, fix_dates
from flights_functions import flight_filter

# SETUP --------------------------------------------------------------------------------------------
# Initiate OpenAI
client = OpenAI()

# Load config files
user_config = configparser.ConfigParser()  # Create a ConfigParser object
user_config.read('josephs_preferences.ini')  # Read the configuration file for the user (me)
# Before pushing to heroku and making work over text, configure api key to be stored in heroku
# Ask chat for help
config = configparser.ConfigParser()
config.read('config.ini')  # Read the config file for passwords and stuff

# Pull the api key from the config file
openai_api_key = config['openai']['api_key']
# Configure the api key
openai.api_key = openai_api_key

# MAIN CODE ------------------------------------------------------------------------------------------
if __name__ == '__main__':
    # STEP 1 - Gather & filter travel request -------------------------------------------------------
    # Imported blank checklist from checklist_logic script

    # Optionally pre-fill in checklist here is desired (Not using now, would need to change chat request)

    # Prompt the user for flight info (For testing purposes, this will be text-based in final version)
    user_input = input("Hello! Tell me about the flight you'd like to book!")

    # Extract relevant flight info from user's message using OpenAI ChatGPT 3.5 API
    updated_checklist = chat_flight_checklist_request_initial(user_input)
    print('\n\nUpdated_checklist! \n')
    print(updated_checklist)
    print('Type', type(updated_checklist))

    # Add code to fix / check the ai results
    updated_checklist['departure_date'] = fix_dates(updated_checklist['departure_date'])
    updated_checklist['return_date'] = fix_dates(updated_checklist['return_date'])

    print('Fixed checklist\n', updated_checklist)

    # Add info to any missing blanks from user's config file / context
    # CODE HERE

    # Check travel request info is complete

    # STEP 2 - Initiate flight search & process request --------------------------------------------
    # Find nearby airports to the destination
    nearby_airports_df = find_nearby_airports(updated_checklist['destination'])
    print('Nearby Airports: \n', nearby_airports_df)
    nearby_airports = nearby_airports_df['code'].tolist()  # This includes the input airport if given one

    # Prepare to collect all flight results in a dictionary
    all_flights_dict = {}

    # Search for flights from home airport to each nearby airport
    for airport in nearby_airports:
        # Create a new filter for each destination airport
        filter = flight_filter(updated_checklist['departure_date'],
                               updated_checklist['home_airport'], airport)
        # Get flights
        result = get_flights(filter)

        # Store the results in the dictionary
        all_flights_dict[airport] = result.flights

    # The price is currently... low/typical/high
    print("The price is currently", result.current_price)

    # Iterate over each destination airport and its flights
    for airport, flights in all_flights_dict.items():
        print(f"\nFlights to {airport}:")

        # Find and print the shortest flight
        shortest_flight = find_shortest_flight(flights)
        print(f"The shortest flight to {airport} is:")
        print(shortest_flight)

        # # Print all flights for this airport
        # for flight in flights:
        #     print(flight)
