from fast_flights import FlightData, Passengers, create_filter, get_flights, Cookies

# Create a new filter
filter1 = create_filter(
    flight_data=[
        # Include more if it's not a one-way trip
        FlightData(
            date="2024-09-25",  # Date of departure
            from_airport="RSW",
            to_airport="DCA"
        ),
        # ... include more for round trips and multi-city trips
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


# Get flights with a filter

result = get_flights(
    filter1,
    dangerously_allow_looping_last_item=True,
    cookies=Cookies.new().to_dict(),
    currency="USD",
    language="en"
)

# The price is currently... low/typical/high
print("The price is currently", result.current_price)

# Display the first flight
print(result.flights[1])

# Loop through and print all flights
for flight in result.flights:
    print(flight)

