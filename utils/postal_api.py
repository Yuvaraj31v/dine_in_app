import requests
from utils.exceptions import BadRequestException


def get_city_state_from_pincode(pincode):
    url = f"https://api.postalpincode.in/pincode/{pincode}"
    try:
        response = requests.get(url, timeout=5)
        data = response.json()
        if data[0]['Status'] == 'Success':
            post_office = data[0]['PostOffice'][0]
            city = post_office['District']
            state = post_office['State']
            return {'city': city, 'state': state}
    except Exception as e:
        print(e)
    return {'city': '', 'state': ''}