import subprocess

import googlemaps

gmaps = googlemaps.Client(key='your_api_key_here')

def get_location():
    location = None
    while location is None:
        try:
            location = gmaps.geolocate()
        except Exception as e:
            print(f"Error getting location; {e}")
    return location


def display_map(location):
    lat = location['location']['lat']
    lng = location['location']['lng']
    url = f"https://www.google.com/maps/search/?api=1&query={lat},{lng}"
    subprocess.call(f"start {url}", shell=True)  # open in default browser
