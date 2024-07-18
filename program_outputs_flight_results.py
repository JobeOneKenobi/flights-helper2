# Functions having to do with the final results printed to the user and sifting through different flight details

def print_flight_info(flight, airline=False, departure=False, arrival=False, duration=False, stops=False):
    '''
    Given a flight item from the flights class / flight results function, and a series of options, prints the flight
    info in an easy to understand format
    :param flight:
    :param airline:
    :param departure:
    :param arrival:
    :param duration:
    :param stops:
    :return:
    '''
    flight_info = ''
