# Main function to run everything right now, still testing locally
from flights.fast_flights import FlightData, Passengers, create_filter, get_flights, Airport
# Importing the entire fast_flights module

import configparser
# My functions
from flight_times import find_shortest_flight
from check_airports import find_nearby_airports

# Load config files
user_config = configparser.ConfigParser()  # Create a ConfigParser object
user_config.read('josephs_preferences.ini')  # Read the configuration file for the user (me)
# Before pushing to heroku and making work over text, configure api key to be stored in heroku
# Ask chat for help
config = configparser.ConfigParser()
config.read('config.ini')  # Read the config file for passwords and stuff

# Start by pulling preferences from user's config file (in this case me)  and other relevant info
home_airport = user_config['basic info']['home_airport']
destination = "DC"


if __name__ == '__main__':
    # Find nearby airports to the destination
    nearby_airports_df = find_nearby_airports(destination)
    print(nearby_airports_df)
    nearby_airports = nearby_airports_df['code'].tolist()  # This includes the input airport if given one

    # Prepare to collect all flight results in a dictionary
    all_flights_dict = {}

    # Search for flights from home airport to each nearby airport
    for airport in nearby_airports:
        # Create a new filter for each destination airport
        filter = create_filter(
            flight_data=[
                FlightData(
                    date="2024-09-02",  # Date of departure
                    from_airport=home_airport,
                    to_airport=airport
                ),
            ],
            trip="one-way",  # Trip (round-trip, one-way, multi-city)
            seat="economy",  # Seat (economy, premium-economy, business or first)
            passengers=Passengers(
                adults=1,
                children=0,
                infants_in_seat=0,
                infants_on_lap=0
            ),
        )

        # Get flights
        result = get_flights(filter)

        # This is the updated functionality for the fast-flights script to enable prices
        # BUT it's currently not working, implement later once I've tested it and it works in seperate script / project
        # # Get flights with the filter
        # result = get_flights(filter,
        #                      dangerously_allow_looping_last_item=True,
        #                      #cookies=Cookies.new().to_dict(),  #Need to figure out where Cookis is stored and referenced
        #                      currency="USD",
        #                      language="en")

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
