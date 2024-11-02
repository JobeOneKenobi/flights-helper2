# Flight Helper

Personal flight search assistant that processes natural language requests to find and evaluate flights across multiple nearby airports.

## Scripts & Functions

### main.py
Status: Working basic functionality
- Main program orchestration 
- Processes user input, searches flights, evaluates results
- Key Function: `if __name__ == '__main__'` handles core program flow

### check_airports.py  
Status: Working
- Handles airport location and nearby airport searching
- Key Functions:
  - `find_nearby_airports(airport_code_or_city)`: Finds international airports within 50mi radius
  - `get_coords_airport(airport_code, airports_df)`: Gets coordinates from airport code
  - `get_coords_city(city_name)`: Gets coordinates from city name

### checklist_logic_ai.py
Status: Working 
- Processes natural language flight requests using GPT-3.5
- Key Functions:
  - `chat_flight_checklist_request_initial(user_message)`: Extracts flight details from user text
  - `fix_dates(input_str)`: Standardizes date formats

### flight_times.py
Status: Needs improvement
- Evaluates and sorts flights based on duration/price
- Key Functions:
  - `find_shortest_flight(flights)`: Finds fastest flight option
  - `check_direct_flights(flights)`: Identifies direct flights
  - `weighted_sort(flights, duration_threshold)`: Sorts flights by duration/price weights

### flights_functions.py 
Status: Working
- Utility functions for flight searching
- Key Function: `flight_filter(flight_date, from_airport, to_airport)`: Creates standardized flight search filter

### program_outputs_flight_results.py
Status: Working
- Handles flight info display formatting
- Key Function: `print_flight_info(flight)`: Formats flight details for output

## Configuration Files

### josephs_preferences.ini
- User preferences for airlines, airports, times etc.
- Includes common city name shortcuts

### config.ini 
- App configuration and API keys

## TODO
- Improve flight evaluation logic
- Add price analysis
- Implement text interface
- Add testing
- Enhance error handling

## Requirements
- OpenAI API key
- Python packages: openai, pandas, geopy, python-dateutil, configparser