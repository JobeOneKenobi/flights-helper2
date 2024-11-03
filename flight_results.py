# STATUS: in progress, first couple filter_by methods WORKING!!

import copy
import pandas as pd
from typing import Dict, List, Optional

from flight_request import FlightRequest


class FlightResults:
    """
    Processes and analyzes flight search results based on user preferences.
    Works in conjunction with FlightRequest to filter and rank flight options.

    The class maintains both original and filtered results, allowing for:
    - Progressive filtering based on multiple criteria
    - Scoring flights based on user preferences
    - Finding best options across multiple airports
    - Resetting to original results if needed
    """

    def __init__(self, raw_results: dict, flight_request: FlightRequest):
        """
        Initialize flight results processor

        Args:
            raw_results (dict): Dictionary of flight results keyed by airport code
            flight_request (FlightRequest): FlightRequest object containing preferences
        """
        self.all_flights_dict = raw_results  # Keep original format
        self.all_flights_df = self._convert_to_dataframe(raw_results)  # Convert for processing
        self.filtered_flights_df = self.all_flights_df.copy()
        self.request = flight_request
        self.best_options = []  # Will store top recommendations
        self._score_cache = {}  # Cache for flight scores

    def _convert_to_dataframe(self, flights_dict):
        """Convert flights dictionary to pandas DataFrame"""
        rows = []
        for airport, flights in flights_dict.items():
            for flight in flights:
                rows.append({
                    'airport_code': airport,
                    'airline': flight.name,
                    'departure': flight.departure,
                    'arrival': flight.arrival,
                    'duration': flight.duration,
                    'stops': flight.stops,
                    'price': float(flight.price.replace('$', '')) if isinstance(flight.price, str) else flight.price
                })
        return pd.DataFrame(rows)

    def filter_by_stops(self, max_stops: Optional[int] = None) -> 'FlightResults':
        """Filter flights by maximum stops"""
        stops_limit = max_stops if max_stops is not None else self.request.max_stops
        self.filtered_flights_df = self.filtered_flights_df[
            self.filtered_flights_df['stops'] <= stops_limit
        ]
        return self

    def filter_by_destination_airport(self, airport_code: str) -> 'FlightResults':
        """
        Filter flights to show only those going to the specified airport.

        Args:
            airport_code (str): Airport code to filter for (e.g., 'DCA', 'BWI')

        Returns:
            FlightResults: Returns self for method chaining
        """
        self.filtered_flights_df = self.filtered_flights_df[
            self.filtered_flights_df['airport_code'] == airport_code.upper()
            ]

        return self

    def filter_by_airlines(self) -> 'FlightResults':
        """
        Apply airline preferences:
        - Remove avoided airlines
        - Prioritize preferred airlines in scoring
        Returns self for method chaining.
        """

    def filter_by_time(self) -> 'FlightResults':
        """
        Filter based on departure_time and arrival_time preferences.
        Returns self for method chaining.
        """

    def _calculate_flight_score(self, flight, airport: str) -> float:
        """
        Calculate a score for a single flight based on how well it matches preferences.
        Uses cached scores when possible.
        """

    def find_best_options(self, num_options: int = 3) -> list:
        """
        Find the best flight options across all airports based on:
        - Preference matching score
        - Price within max_price_difference
        - Airport convenience
        """

    def reset_filters(self):
        """Reset filtered_flights to original state"""
        self.filtered_flights = self.all_flights.copy()
        return self

    def get_results(self, format='dataframe'):
        """Get results in desired format"""
        if format == 'dataframe':
            return self.filtered_flights_df
        elif format == 'dict':
            # Convert back to dictionary format
            results_dict = {}
            for airport in self.filtered_flights_df['airport_code'].unique():
                airport_flights = self.filtered_flights_df[
                    self.filtered_flights_df['airport_code'] == airport
                ]
                results_dict[airport] = airport_flights.to_dict('records')
            return results_dict