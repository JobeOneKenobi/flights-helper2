# Class definition for a flight request object, similar to a user in J.O.E.

import configparser
from pprint import pprint

import openai
from openai import OpenAI

from checklist_logic_ai import chat_flight_checklist_request_initial


# main execution script to initiate a flight request and loop until sufficient user data has been supplied
def initiate_flight_request(user_input_raw, active_flight_request=None):
    # arg: user_input_raw: user message hopefully containing flight info
    # arg: active_flight_request, active flight request object, if any exists
    # return: prompt / message to user about what data is needed
    # return flight_request.is_complete():: TRUE / FALSE
    # return flight_request object
    client = OpenAI()

    # REMOVE ALL THIS CONFIG STUFF B4 PUSHING TO SERVER
    # Before pushing to heroku and making work over text, configure api key to be stored in heroku
    # Ask chat for help
    config = configparser.ConfigParser()
    config.read('config.ini')

    # Pull the api key from the config file
    openai_api_key = config['openai']['api_key']
    # Configure the api key
    openai.api_key = openai_api_key

    # Initiates a new flight_request object if none is active
    if not active_flight_request:
        flight_request = FlightRequest()
    else:
        flight_request = active_flight_request

    # Extract key values from user message using open ai api filter function
    ai_sifted_input_data = chat_flight_checklist_request_initial(user_input_raw)

    # Only update values in object if key exists and has a non-None value
    for field in ['home_airport', 'destination', 'departure_date', 'return_date']:
        if field in ai_sifted_input_data and ai_sifted_input_data[field] not in [None, "null"]:
            flight_request.add_basic_data(**{field: ai_sifted_input_data[field]})

    # If still missing data, request what's missing
    if not flight_request.is_complete():
        response_message = f"Please provide flight info (missing: {flight_request.get_missing_fields()}): "
    else:
        response_message = ''

    return response_message, flight_request.is_complete(), flight_request


class FlightRequest:
    """
    Simple class to store and organize flight request data.

    Required:
    - home_airport: departure airport code (str)
    - destination: destination airport code (str)
    - departure_date: when you want to leave (str)
    - return_date: when you want to come back, None if one-way (str)

    Optional:
    - departure_time: preferred time of day (str)
    - arrival_time: preferred arrival time (str)
    - airlines_preferred: list of airlines you like (list)
    - airlines_avoid: list of airlines you don't like (list)
    - max_stops: maximum number of stops (int)
    - airports_avoid: airports to avoid (list)
    - baggage_preference: baggage needs (str)
    - min_layover_length: shortest acceptable layover in minutes (int)
    - max_price_difference: max extra $ you'll pay for better flight (float)
    - departure_date_flexible: whether dates can vary (bool)
    - return_date_flexible: whether return dates can vary (bool)
    """

    def __init__(self):
        # Required fields start as None
        self.home_airport = None
        self.destination = None
        self.departure_date = None

        # Optional stuff with defaults
        self.return_date = None  # Optional, can stay None for one-way
        self.departure_time = "any"
        self.arrival_time = "any"
        self.airlines_preferred = []
        self.airlines_avoid = []
        self.max_stops = 99
        self.airports_avoid = []
        self.baggage_preference = "any"
        self.min_layover_length = 45
        self.max_price_difference = 100.0
        self.departure_date_flexible = 0
        self.return_date_flexible = 0

    def to_dict(self):
        """Convert flight request to dictionary"""
        return {
            'home_airport': self.home_airport,
            'destination': self.destination,
            'departure_date': self.departure_date,
            'return_date': self.return_date,
            'departure_time': self.departure_time,
            'arrival_time': self.arrival_time,
            'airlines_preferred': self.airlines_preferred,
            'airlines_avoid': self.airlines_avoid,
            'max_stops': self.max_stops,
            'airports_avoid': self.airports_avoid,
            'baggage_preference': self.baggage_preference,
            'min_layover_length': self.min_layover_length,
            'max_price_difference': self.max_price_difference,
            'departure_date_flexible': self.departure_date_flexible,
            'return_date_flexible': self.return_date_flexible
        }

    def from_dict(self, data):
        """Update flight request from dictionary"""
        for key, value in data.items():
            if hasattr(self, key):
                setattr(self, key, value)

    def add_basic_data(self, home_airport=None, destination=None, departure_date=None, return_date=None):
        """Add basic flight data from user input"""
        if home_airport: self.home_airport = home_airport.upper()
        if destination: self.destination = destination.upper()
        if departure_date: self.departure_date = departure_date
        if return_date: self.return_date = return_date

    def is_complete(self):
        """Check if minimum required data is present"""
        required_fields = [
            self.home_airport,
            self.destination,
            self.departure_date
        ]
        return all(field is not None for field in required_fields)

    def get_missing_fields(self):
        """Return list of missing required fields"""
        missing = []
        if not self.home_airport: missing.append('home_airport')
        if not self.destination: missing.append('destination')
        if not self.departure_date: missing.append('departure_date')
        return missing

    def load_preferences(self, ini_file='josephs_preferences.ini'):
        """Load preferences from ini file for any unset values"""
        config = configparser.ConfigParser()
        config.read(ini_file)

        # Load home airport from basic info if not set
        if 'basic info' in config and not self.home_airport:
            self.home_airport = config['basic info'].get('home_airport')

        # Load preferences section
        if 'preferences' in config:
            prefs = config['preferences']

            # Only load each preference if not already set to non-default value
            if self.departure_time == "any":
                self.departure_time = prefs.get('departure_time', self.departure_time)

            if self.arrival_time == "any":
                self.arrival_time = prefs.get('arrival_time', self.arrival_time)

            if not self.airlines_preferred and 'airlines_preferred' in prefs:
                self.airlines_preferred = [x.strip() for x in prefs['airlines_preferred'].split(',')]

            if not self.airlines_avoid and 'airlines_avoid' in prefs:
                self.airlines_avoid = [x.strip() for x in prefs['airlines_avoid'].split(',')]

            if self.max_stops == 99 and 'stops' in prefs:
                self.max_stops = int(prefs['stops'])

            if not self.airports_avoid and 'airports_avoid' in prefs:
                self.airports_avoid = [x.strip() for x in prefs['airports_avoid'].split(',')]

            if self.baggage_preference == "any":
                self.baggage_preference = prefs.get('baggage', self.baggage_preference)

            if self.min_layover_length == 45 and 'layover_length' in prefs:
                layover = prefs['layover_length']
                if 'hr' in layover:
                    hours = float(layover.split('hr')[0].strip())
                    self.min_layover_length = int(hours * 60)

            if self.max_price_difference == 100.0 and 'price_difference' in prefs:
                price = prefs['price_difference'].strip('$')
                self.max_price_difference = float(price)


if __name__ == '__main__':
    # # Basic creation and checking
    # request = FlightRequest()
    # print("Empty request missing fields:", request.get_missing_fields())
    #
    # # Add partial data
    # request.add_basic_data(destination="LAX", departure_date="2024-06-15")
    # print("\nAfter adding destination and date:")
    # print("Missing fields:", request.get_missing_fields())
    # print("Is complete?", request.is_complete())
    #
    # # Load preferences (should get home_airport=RSW from your ini)
    # request.load_preferences()
    # print("\nAfter loading preferences:")
    # print("Home airport:", request.home_airport)
    # print("Missing fields:", request.get_missing_fields())
    # print("Is complete?", request.is_complete())
    #
    # # Check what preferences got loaded
    # print("\nPreference details:")
    # print("Airlines preferred:", request.airlines_preferred)
    # print("Max stops:", request.max_stops)
    # print("Layover length (mins):", request.min_layover_length)
    #
    # # Test dict conversion
    # request_dict = request.to_dict()
    # print("\nDictionary version:")
    # pprint(request_dict)
    #
    # # Test creating new request from dict
    # new_request = FlightRequest()
    # new_request.from_dict(request_dict)
    # print("\nNew request from dict - airlines:", new_request.airlines_preferred)

    ###
    # client = OpenAI()
    #
    # # Before pushing to heroku and making work over text, configure api key to be stored in heroku
    # # Ask chat for help
    # config = configparser.ConfigParser()
    # config.read('config.ini')
    #
    # # Pull the api key from the config file
    # openai_api_key = config['openai']['api_key']
    # # Configure the api key
    # openai.api_key = openai_api_key
    #
    # newrequest = FlightRequest()
    #
    # while not newrequest.is_complete():
    #     user_message = input(f"Please provide flight info (missing: {newrequest.get_missing_fields()}): ")
    #     ai_sifted_input_data = chat_flight_checklist_request_initial(user_message)
    #
    #     # Only update if key exists and has a non-None value
    #     for field in ['home_airport', 'destination', 'departure_date', 'return_date']:
    #         if field in ai_sifted_input_data and ai_sifted_input_data[field] not in [None, "null"]:
    #             newrequest.add_basic_data(**{field: ai_sifted_input_data[field]})
    #
    # print("Flight request complete!")
    #
    # pprint(newrequest.to_dict())
    #
    # print(newrequest.destination)
    # print(newrequest.airlines_preferred)
    # newrequest.airlines_preferred = ['southwest']
    # print(newrequest.airlines_preferred)

    request_complete = False
    prompt = 'input some flight info'
    current_flight_request = None

    while request_complete is not True:
        user_input = input(prompt)
        prompt, current_flight_request, request_complete = initiate_flight_request(user_input, current_flight_request)
