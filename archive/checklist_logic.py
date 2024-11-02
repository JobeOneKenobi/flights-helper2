# Functions to do with the flight checklist and other logic
# In progress -> ACTIVELY being worked on
# STATUS: basic working, needs good bit of work though
# This could be a use case for chatGPT-4 / plus, or maybe even community
    # Tested it briefly with 3.5 and it worked well

import re
from datetime import datetime
from dateutil import parser

checklist = {
    'home_airport': None,
    'destination': None,
    'departure_date': None,
    'return_date': None,
    'airline_preference': None,
}


def is_airport(input_str):
    # Assuming IATA codes are three letters
    return re.match(r'^[A-Z]{3}$', input_str.upper())


# Currently working on
# STATUS: basic working, needs good bit of work though
# This could be a use case for chatGPT-4 / plus, or maybe even community
def is_date(input_str):
    try:
        # Attempt to parse the date
        parsed_date = parser.parse(input_str, fuzzy=True, default=datetime.now())

        # Standardize the date format to YYYY-MM-DD
        standardized_date = parsed_date.strftime('%Y-%m-%d')

        return standardized_date
    except (ValueError, OverflowError):
        return None


def categorize_input(input_str):
    if is_airport(input_str):
        return 'airport'
    elif is_date(input_str):
        return 'date'
    # Add more conditions as needed
    else:
        return 'unknown'


def prompt_user_for_info():
    while None in checklist.values():
        user_input = input("Please provide the missing information: ")

        category = categorize_input(user_input)

        # print(checklist.values())

        if category == 'airport':
            if checklist['home_airport'] is None:
                checklist['home_airport'] = user_input.upper()
                # print(f"Home airport set to {user_input.upper()}")
            elif checklist['destination'] is None:
                checklist['destination'] = user_input.upper()
                # print(f"Destination set to {user_input.upper()}")
        elif category == 'date':
            if checklist['departure_date'] is None:
                checklist['departure_date'] = user_input
                # print(f"Departure date set to {user_input}")
            elif checklist['return_date'] is None:
                checklist['return_date'] = user_input
                # print(f"Return date set to {user_input}")
        else:
            pass
            # print("Input not recognized. Please try again.")

    # print("All required information has been provided.")


if __name__ == '__main__':
    prompt_user_for_info()
    # Now you can use the filled checklist to run your search logic
    print("Final checklist:", checklist)

    # Your existing logic to process the checklist and run the search
    home_airport = checklist['home_airport']
    destination = checklist['destination']
    departure_date = checklist['departure_date']
    return_date = checklist['return_date']
    airline = checklist.get('airline')
    seat_class = checklist.get('seat_class')

    # Example usage of the collected data
    print(f"Searching flights from {home_airport} to {destination} on {departure_date}.")
    if return_date:
        print(f"Returning on {return_date}.")
    if airline:
        print(f"Preferred airline: {airline}.")
    if seat_class:
        print(f"Seat class: {seat_class}.")
