# Main function to run everything right now, still testing locally
from flights.fast_flights import FlightData, Passengers, create_filter, get_flights, Airport
# Importing the entire fast_flights module

import configparser
import openai
from openai import OpenAI
import pandas as pd
import logging

# My functions
from flight_times import find_shortest_flight
from check_airports import find_nearby_airports
from checklist_logic_ai import chat_flight_checklist_request_initial, fix_dates, checklist
from flights_functions import flight_filter
from flight_times import weighted_sort
from program_outputs_flight_results import print_flight_info

# For whatever reason this syntax works for setting logging level and the other does not
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Use this to test logging if logging.info not working
# logging.warning('Watch out!')  # will print a message to the console

# SETUP --------------------------------------------------------------------------------------------
# Initiate OpenAI
client = OpenAI()

# Load config files
user_config = configparser.ConfigParser()  # Create a ConfigParser object
user_config.read('josephs_preferences.ini')  # Read the configuration file for the user (me)
# Before pushing to heroku and making work over text, update it to use api key stored in heroku

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

    # Optionally pre-fill in checklist here if desired (Not using now, would need to change chat request)

    # Prompt the user for flight info (For testing purposes, this will be text-based in final version)
    # user_input = input("Hello! Tell me about the flight you'd like to book!")
    user_input = "RSW to DCA 9/13 - 9/15"
    shortest_flights_dict = {}

    # Extract relevant flight info from user's message using OpenAI ChatGPT 4o mini API
    updated_checklist = chat_flight_checklist_request_initial(user_input)
    logging.info(f"Updated Checklist: \n {updated_checklist}")

    # Add code to fix / check the AI results
    updated_checklist['departure_date'] = fix_dates(updated_checklist['departure_date'])
    updated_checklist['return_date'] = fix_dates(updated_checklist['return_date'])

    # Add info to any missing blanks from user's config file / context
    # Pulls default home airport if none found / stated in user's request
    if updated_checklist['home_airport'] is None:
        updated_checklist['home_airport'] = user_config['basic info']['home_airport']

    logging.info(f'\nFormatted checklist\n {updated_checklist}')

    # CODE HERE

    # Check travel request info is complete

    # Add code to fill in / check / adjust checklist / flight info based off user's preferences file, or in this
    # case my preference file

    # STEP 2 - Initiate flight search & process request --------------------------------------------
    # Find nearby airports to the destination
    nearby_airports_df = find_nearby_airports(updated_checklist['destination'])
    print('\nNearby Airports: \n', nearby_airports_df)
    nearby_airports = nearby_airports_df['code'].tolist()  # This includes the input airport if given one

    # Prepare to collect all flight results in a dictionary
    all_flights_dict = {}

    # Search for flights from home airport to each nearby airport
    for airport in nearby_airports:
        # Create a new filter for each destination airport
        filter_for_airport = flight_filter(updated_checklist['departure_date'],
                                           updated_checklist['home_airport'], airport)

        # Get flights
        result = get_flights(filter_for_airport)

        # Store the results in the dictionary
        all_flights_dict[airport] = result.flights

    # Read / extract the dictionary into a pandas dataframe then save it to a csv?
    # Not positive on these two lines of code
    df_flights = pd.DataFrame(all_flights_dict.items())
    df_flights.to_csv('flights_output.csv', index=False)

    # Display / Return Results ---------------------------------------------------------------------------------
    print('\n------------------Flight Results---------------\n')
    # Iterate over each destination airport and its flights
    for airport, flights in all_flights_dict.items():
        print(f"\nFlights to {airport}:")

        # Find and print the shortest flight
        print(f"The shortest flight to {airport} is:")
        shortest_flight_iter = find_shortest_flight(flights)  # Finds the shortest flight to this airport

        # Prints shortest flight info
        print_flight_info(shortest_flight_iter, show_duration=True)

        # Saves the shortest flight and the airport to a new data structure / dict
        shortest_flights_dict[airport] = shortest_flight_iter  # IDK if I'll need this but leave for now, one method to

    # For the purposes of storing or further processing the top 3 flights,
    # You might want to structure shortest_flights_dict differently, if needed.

    # -----------------------------------------------------------------------------------------------------------






    # OTHER CODE / OLD

        # store favorite flights
        # print(all_flights_dict.items)

        # # Print all flights for this airport
        # for flight in flights:
        #     print(flight)

    # # for testing just one flight entry
    # filter = get_flights(updated_checklist['departure_date'],
    #                        updated_checklist['home_airport'], updated_checklist['destination'])

    # Un-formatted flight info
    # print(all_flights_dict['SNA'][0])

    # Formatted flight info
    # print_flight_info(all_flights_dict['SNA'][0])
