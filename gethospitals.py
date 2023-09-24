import requests

def get_nearest_hospitals(postal_code, api_key):
    geocode_url = f"https://maps.googleapis.com/maps/api/geocode/json?address={postal_code}&key={api_key}"
    geocode_response = requests.get(geocode_url).json()
    location = geocode_response['results'][0]['geometry']['location']
    lat, lng = location['lat'], location['lng']

    places_url = f"https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={lat},{lng}&radius=5000&type=hospital&key={api_key}"
    places_response = requests.get(places_url).json()

    hospitals = places_response['results'][:3]
    hospital_info = []
    for hospital in hospitals:
        name = hospital['name']
        address = hospital['vicinity']
        # Get the phone number of the hospital
        place_id = hospital['place_id']
        details_url = f"https://maps.googleapis.com/maps/api/place/details/json?place_id={place_id}&fields=formatted_phone_number&key={api_key}"
        details_response = requests.get(details_url).json()
        phone_number = details_response['result'].get('formatted_phone_number', 'Phone number not available')
        hospital_info.append((name, address, phone_number))

    return hospital_info


# Replace 'YOUR_API_KEY' with your actual Google Maps API key
api_key = ''
postal_code = '123456'
#hospital_info = get_nearest_hospitals(postal_code, api_key)
#for info in hospital_info:
#    print(f"Name: {info[0]}, Address: {info[1]}, Phone Number: {info[2]}")
