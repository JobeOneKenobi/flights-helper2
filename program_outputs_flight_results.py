# Functions having to do with the final results printed to the user and sifting through different flight details


def print_flight_info(flight, show_airline=True, show_departure=True, show_arrival=True, show_stops=True,
                      show_duration=False, show_price=True):
    """
    Prints flight information in a customizable format.

    Parameters:
    flight (Flight): A Flight object containing the flight information.
    show_airline (bool): Whether to show the airline name. Default is True.
    show_departure (bool): Whether to show the departure time and date. Default is True.
    show_arrival (bool): Whether to show the arrival time and date. Default is True.
    show_stops (bool): Whether to show the number of stops. Default is True.
    """
    parts = []

    if show_airline:
        parts.append(f"{flight.name}")

    if show_departure:
        parts.append(f"departing {flight.departure}")

    if show_arrival:
        parts.append(f"arriving {flight.arrival}")

    if show_stops:
        parts.append(f"{flight.stops} stop(s)")

    if show_duration:
        parts.append(f"{flight.duration} total.")

    if show_price:
        parts.append(f"Price: {flight.price}")

    flight_info = ', '.join(parts)
    print(flight_info)


