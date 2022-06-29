import time
from geopy.geocoders import Nominatim

geolocator = Nominatim(user_agent='geopyExercises')

def get_data(x):

    # Each item will create an index and a row, that is the content
    index, row = x

    # Interval between actions
    time.sleep(3)

    # Requesting on API and saving to a variable
    response = geolocator.reverse(row['query'])
    address = response.raw['address']

    # Acessing the information and saving it to a variable
    place_id = response.raw['place_id'] if 'place_id' in response.raw else 'NA'
    osm_type = response.raw['osm_type'] if 'osm_type' in response.raw else 'NA'
    country = response.raw['address']['country'] if 'country' in address else 'NA'
    country_code = response.raw['address']['country_code'] if 'country_code' in address else 'NA'

    return place_id, osm_type, country, country_code
