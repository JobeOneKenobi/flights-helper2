# Place for storing modified or added on to fast-flights functions and classes
from flights.fast_flights import FlightData, Passengers, create_filter, get_flights


def flight_filter(flight_date, from_airport, to_airport):
    '''
    Fast-flights flight filter function with pre-entered in data
    :param flight_date:
    :param from_airport:
    :param to_airport:
    :return:
    '''
    filter = create_filter(
        flight_data=[
            FlightData(
                date=flight_date,  # Date of departure
                from_airport=from_airport,
                to_airport=to_airport
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
    return filter