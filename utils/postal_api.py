import requests
from utils.exceptions import BadRequestException
from requests.exceptions import RequestException, Timeout, HTTPError, ConnectionError


def get_city_state_from_pincode(pincode):
    url = f"https://api.postalpincode.in/pincode/{pincode}"
    try:
        response = requests.get(url, timeout=5)
        data = response.json()
        if data[0]['Status'] == 'Success':
            city = data[0]['PostOffice'][0]['District']
            state = data[0]['PostOffice'][0]['State']
            return {'city': city, 'state': state}
    except (Timeout, ConnectionError) as e:
        BadRequestException(f"Network-related error: {e}")
    except ValueError as e:
        BadRequestException(f"Invalid JSON response: {e}")
    except (KeyError, IndexError, TypeError) as e:
        BadRequestException(f"Unexpected data structure: {e}")

    return {'city': '', 'state': ''}