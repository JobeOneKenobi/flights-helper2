# functions for evaluating which flights are best

# first determine if there are direct flights

# functionality to add later:
# compare price of direct flights to connecting ones

from typing import List, Tuple
from fast_flights import Flight
import logging
import random

# Import timedelta for comparing time differences
from datetime import timedelta

# These are new and need to be worked on / improved
# They are complete shit, start from scratch and come up with a smart way to do flight sorting
# ---------------------------------------------------------------------------------------------------------------


# Helper function to convert flight duration to timedelta for comparison
def convert_to_timedelta(duration):
    """
    Converts flight duration to timedelta for comparison.
    Assumes duration is in minutes. Adjust if needed.
    """
    return timedelta(minutes=duration)


def custom_sort_key(flight):
    """
    Custom sort key function to prioritize flights based on duration and price.
    """
    return (convert_to_minutes(flight.duration), flight.price)


# Function to sort flights with weighted consideration for duration and price
def weighted_sort(flights, duration_threshold=30):
    """
    Sort flights with a weighted consideration for duration and price.
    If flight durations are within 'duration_threshold' minutes, sort by price.
    Otherwise, sort primarily by duration.

    :param flights: List of flight objects.
    :param duration_threshold: Maximum difference in duration (in minutes) to consider for price sorting.
    :return: Sorted list of flights.
    """
    # Initialize a list to store converted durations and handle any errors
    converted_durations = []

    for flight in flights:
        try:
            # Attempt to convert the flight duration to minutes
            duration_minutes = convert_to_minutes(flight.duration)
            converted_durations.append((flight, duration_minutes))
        except ValueError as e:
            # Log the error for debugging purposes
            logging.error(f"Error converting duration for flight {flight}: {e}")
            # Assign a high default duration (e.g., 9999 minutes) or random value
            converted_durations.append((flight, 9999))

    # Find the minimum duration among the successfully converted durations
    min_duration = min(duration for flight, duration in converted_durations if duration != 9999)

    # Sort the flights using a custom key with weighted logic
    return sorted(converted_durations, key=lambda item: (
        item[0].price if abs(item[1] - min_duration) <= duration_threshold else item[1]
    ))


# Probably replace this with a ChatGPT call to make it more robust, but check format, may be simple
def convert_to_minutes(duration_str):
    """
    Converts a duration string (like '2 hr 29 min', '1h 30m', '90m', or '2h') to total minutes.
    Handles various formats and adds error handling for unexpected strings.
    """
    try:
        # Check if the string has 'hr' and 'min' (e.g., '2 hr 29 min')
        if 'hr' in duration_str and 'min' in duration_str:
            hours, minutes = duration_str.split('hr')
            hours = hours.strip()
            minutes = minutes.strip().replace('min', '').strip()
            return int(hours) * 60 + int(minutes)

        # Check if the string has only 'hr' (e.g., '2 hr')
        elif 'hr' in duration_str:
            hours = duration_str.replace('hr', '').strip()
            return int(hours) * 60

        # Check if the string has only 'h' and 'm' (e.g., '1h 30m')
        elif 'h' in duration_str and 'm' in duration_str:
            hours, minutes = duration_str.split('h')
            minutes = minutes.strip().replace('m', '')
            return int(hours.strip()) * 60 + int(minutes)

        # Check if the string has only 'h' (e.g., '2h')
        elif 'h' in duration_str:
            hours = duration_str.replace('h', '').strip()
            return int(hours) * 60

        # Check if the string has only 'm' (e.g., '90m')
        elif 'm' in duration_str:
            minutes = duration_str.replace('m', '').strip()
            return int(minutes)

        # Check if the string contains only numbers
        elif duration_str.strip().isdigit():
            return int(duration_str)

        else:
            # Log error for any unsupported format
            logging.error(f"Unsupported duration format: '{duration_str}'")
            raise ValueError(f"Cannot convert duration string to minutes: '{duration_str}'")

    except ValueError as e:
        # Log error and raise it for further investigation
        logging.error(f"Invalid duration format '{duration_str}': {e}")
        raise ValueError(f"Cannot convert duration string to minutes: '{duration_str}'") from e

# ----------------------------------------------------------------------------------------------------------------


def find_shortest_flight(flights: List[Flight]) -> Flight:
    """
    Finds the flight with the shortest trip time in the provided list of flights.

    Args:
       flights (List[Flight]): List of Flight objects.

    Returns:
       Flight: The Flight object with the shortest trip time.
    """
    # Combine logic for duration conversion and finding minimum in one step
    shortest_flight = min(flights, key=lambda flight:
    int(flight.duration.split()[0] if 'hr' in flight.duration else 0) * 60 +
    int(flight.duration.split()[2] if 'min' in flight.duration else 0))

    return shortest_flight


def check_direct_flights(flights: List[Flight]) -> Tuple[bool, List[Flight]]:
    """
    Check if there are any direct flights in the provided list of flights.

    Args:
        flights (List[Flight]): List of Flight objects.

    Returns:
        Tuple[bool, List[Flight]]: A tuple containing a boolean indicating if there are direct flights
                                   and a list of direct Flight objects.
    """
    direct_flights = [flight for flight in flights if flight.stops == 0]
    return (len(direct_flights) > 0, direct_flights)
