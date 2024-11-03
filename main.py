# Main function to run everything right now, still testing locally
from flights.fast_flights import FlightData, Passengers, create_filter, get_flights, Airport
# Importing the entire fast_flights module

import configparser
import openai
from openai import OpenAI
import pandas as pd
import logging
import pprint

# My functions
from evaluate_flight_times import find_shortest_flight
from check_airports import find_nearby_airports
from checklist_logic_ai import chat_flight_checklist_request_initial, fix_dates, checklist
from flights_functions import flight_filter
from evaluate_flight_times import weighted_sort
from program_outputs_flight_results import print_flight_info
from flight_request import FlightRequest, initiate_flight_request
from flight_results import FlightResults

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


def process_flight_request_master_function():
    # STEP 1 - Gather & filter travel request -------------------------------------------------------
    request_complete = False
    prompt = 'input some flight info'
    current_flight_request = None

    while request_complete is not True:
        user_input = input(prompt)  # This portion will need to be updated later
        prompt, request_complete, current_flight_request = initiate_flight_request(user_input, current_flight_request)
        logger.info(prompt)
        logger.debug(current_flight_request.to_dict())
        logger.info(request_complete)

    # STEP 1B - Format data properly
    if current_flight_request.departure_date:
        current_flight_request.departure_date = fix_dates(current_flight_request.departure_date)

    logging.info(f'\nFormatted flight request data\n {current_flight_request.to_dict}')

    # STEP 2 - Initiate flight search & process request --------------------------------------------
    # Find nearby airports to the destination
    nearby_airports_df = find_nearby_airports(current_flight_request.destination)
    print('\nNearby Airports: \n', nearby_airports_df)
    nearby_airports = nearby_airports_df['code'].tolist()  # This includes the input airport if given one

    # Prepare to collect all flight results in a dictionary
    shortest_flights_dict = {}
    all_flights_dict = {}

    # Search for flights from home airport to each nearby airport
    for airport in nearby_airports:
        # Create a new filter for each destination airport
        filter_for_airport = flight_filter(current_flight_request.departure_date,
                                           current_flight_request.home_airport, airport)

        # Get flights
        result = get_flights(filter_for_airport)

        # Store the results in the dictionary
        all_flights_dict[airport] = result.flights

    # Initialize FlightResults with your dictionary of flights
    flight_results = FlightResults(all_flights_dict, current_flight_request)

    # Example of using multiple filters
    filtered_results = (flight_results
                        .filter_by_stops(0)  # Uses max_stops from your preferences
                        .filter_by_destination_airport('DCA')
                        .get_results())  # Get as DataFrame

    # STATUS: WORKING
    # TODO: add much more functionality to FlightResults class and make a seperate class / module for ai powered
    # flight comparison
    # Print more useful information
    print("\n-----------------Filtered Flight Results----------------\n")
    print(f"Found {len(filtered_results)} flights matching criteria:")
    pd.set_option('display.max_columns', None)  # Show all columns
    pd.set_option('display.expand_frame_repr', False)  # Prevent wrapping
    print(filtered_results[['airline', 'departure', 'arrival', 'duration', 'stops', 'price']])

    # Display / Return Results ---------------------------------------------------------------------------------
    # print('\n------------------Flight Results---------------\n')
    # # Iterate over each destination airport and its flights
    # for airport, flights in all_flights_dict.items():
    #     print(f"\nFlights to {airport}:")
    #
    #     # Find and print the shortest flight
    #     print(f"The shortest flight to {airport} is:")
    #     shortest_flight_iter = find_shortest_flight(flights)  # Finds the shortest flight to this airport
    #
    #     # Prints shortest flight info
    #     print_flight_info(shortest_flight_iter, show_duration=True)
    #
    #     # Saves the shortest flight and the airport to a new data structure / dict
    #     shortest_flights_dict[airport] = shortest_flight_iter  # IDK if I'll need this but leave for now, one method to
    #
    # # For the purposes of storing or further processing the top 3 flights,
    # # You might want to structure shortest_flights_dict differently, if needed.

    # -----------------------------------------------------------------------------------------------------------


# MAIN CODE ------------------------------------------------------------------------------------------
if __name__ == '__main__':
    process_flight_request_master_function()
    logger.info('DONE!')
