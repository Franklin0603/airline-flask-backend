
### Passenger table
    - Passenger ID (Primary Key)
    - First Name
    - Last Name
    - Gender
    - Age
    - Nationality

### Airport
    - Airport Name (Primary Key)
    - Airport Country Code
    - Country Name
    - Airport Continent

### Flight
    Flight ID (Primary Key)
    Departure Date
    Flight Status
    Flight ID (Foreign Key)
    Passenger ID (Foreign Key)
    Arrival Airport
    Pilot Name  

import pandas as pd
airline_raw = pd.read_csv("../data/raw/Airline Dataset.csv")
columns = ['Passenger ID', 'First Name', 'Last Name', 'Gender', 'Age',
           'Nationality', 'Airport Name', 'Airport Country Code']
# passenger_raw = airline_raw[columns].sort_values(['Last Name']).head(10)
passenger_raw = airline_raw[columns].drop_duplicates()
passenger_raw.head()

columns = ['Airport Name', 'Airport Country Code', 'Country Name',
           'Airport Continent', 'Continents']
airport_raw = airline_raw[columns].drop_duplicates()
airport_raw.head()

# remove bad data from airport.

# List of airports and their correct details
correct_airports = [
    {
        'Airport Name': 'San Pedro Airport',
        'Airport Country Code': 'BZ',
        'Country Name': 'Belize',
        'Airport Continent': 'NAM',
        'Continents': 'North America'
    },
    {
        'Airport Name': 'San Javier Airport',
        'Airport Country Code': 'ES',
        'Country Name': 'Spain',
        'Airport Continent': 'EU',
        'Continents': 'Europe'
    }
]

# Loop through each airport and its correct details
for airport in correct_airports:
    airport_raw = airport_raw[(airport_raw['Airport Name'] != airport['Airport Name']) | 
                              ((airport_raw['Airport Name'] == airport['Airport Name']) & 
                               (airport_raw['Airport Country Code'] == airport['Airport Country Code']) & 
                               (airport_raw['Country Name'] == airport['Country Name']) & 
                               (airport_raw['Airport Continent'] == airport['Airport Continent']) & 
                               (airport_raw['Continents'] == airport['Continents']))]

# unique_combo = airport_raw['Airport Name'] + '-' + airport_raw['Airport Country Code']
unique_combo = airport_raw[['Airport Name', 'Airport Country Code']].apply('-'.join, axis=1)
is_unique_combo = unique_combo.is_unique

# Add IDs based on the uniqueness
if is_unique_combo:
    airport_raw['Airport_ID'] = range(1, len(airport_raw) + 1)
else:
    # If there are duplicate combinations, create a unique ID for each 'Airport Name'
    unique_airports = airline_raw['Airport Name'].unique()
    airport_ids = { name:idx for idx, name in enumerate(unique_airports, 1)}
    # I need to fix this - there is a bug there
    airport_raw['Airport_ID'] = airport_raw['Airport Name'].map(airport_ids)


columns = ['Airport Name','Airport Country Code','Departure Date', 'Arrival Airport',
           'Pilot Name', 'Flight Status']
flight_raw = airline_raw[columns]
flight_raw.head()    

import pandas as pd
import hashlib

# Create unique_combo using join
unique_combo = flight_raw[['Airport Name', 'Arrival Airport', 'Pilot Name', 'Flight Status']].apply('-'.join, axis=1)
is_unique_combo = unique_combo.is_unique

# Add IDs based on the uniqueness
if is_unique_combo:
    flight_raw['Flight_ID'] = range(1, len(flight_raw) + 1)
else:
    # Generate unique IDs using a hash function
    flight_raw['Flight_ID'] = [int(hashlib.sha256(val.encode()).hexdigest(), 16) % 10**8 for val in unique_combo]

merged_flight_airport = pd.merge(flight_raw, airport_raw, on=['Airport Name', 'Airport Country Code'])
final_merged_table = pd.merge(merged_flight_airport, passenger_raw, on=['Airport Name', 'Airport Country Code'])

final_merged_table.columns

columns = ['Passenger ID', 'First Name', 'Last Name', 'Gender', 'Age','Nationality']
passenger_raw_final = final_merged_table[columns]
passenger_raw_final.head()

columns = ['Airport_ID','Airport Name', 'Airport Country Code', 'Country Name', 'Airport Continent','Continents']
airline_raw_final = final_merged_table[columns]
airline_raw_final.head()

columns = ['Flight_ID','Departure Date','Arrival Airport', 'Pilot Name', 'Flight Status', 
       'Country Name', 'Airport_ID','Passenger ID']
flight_raw_final = final_merged_table[columns]
flight_raw_final.head()